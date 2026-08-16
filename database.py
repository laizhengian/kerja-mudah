import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="data/data.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, timeout=10)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA busy_timeout=5000")
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                job_code TEXT UNIQUE,
                item TEXT NOT NULL,
                problem TEXT,
                quote REAL DEFAULT 0,
                status TEXT DEFAULT 'pending',
                due_date TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                purpose TEXT,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                invoice_code TEXT UNIQUE,
                amount REAL NOT NULL,
                paid INTEGER DEFAULT 0,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER DEFAULT 0,
                min_quantity INTEGER DEFAULT 5,
                unit_price REAL DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_customer_id ON jobs(customer_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_due_date ON jobs(due_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_invoices_job_id ON invoices(job_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_invoices_paid ON invoices(paid)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_appointments_customer_id ON appointments(customer_id)")
        self.conn.commit()
        
    def set_setting(self, key, value):
        self.conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()
        
    def get_setting(self, key, default=None):
        cursor = self.conn.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        )
        row = cursor.fetchone()
        return row["value"] if row else default
        
    def remove_setting(self, key):
        self.conn.execute("DELETE FROM settings WHERE key = ?", (key,))
        self.conn.commit()
        
    def add_customer(self, name, phone=None, email=None, address=None, notes=None):
        cursor = self.conn.execute(
            "INSERT INTO customers (name, phone, email, address, notes) VALUES (?, ?, ?, ?, ?)",
            (name, phone, email, address, notes)
        )
        self.conn.commit()
        return cursor.lastrowid
        
    def get_customers(self, search=None):
        if search:
            return self.conn.execute(
                "SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ? ORDER BY name",
                (f"%{search}%", f"%{search}%")
            ).fetchall()
        return self.conn.execute("SELECT * FROM customers ORDER BY name").fetchall()
        
    def get_customer(self, customer_id):
        return self.conn.execute(
            "SELECT * FROM customers WHERE id = ?", (customer_id,)
        ).fetchone()
        
    def add_job(self, customer_id, item, problem, quote, due_date, notes=None):
        for attempt in range(10):
            job_code = f"JOB-{datetime.now().strftime('%Y%m%d')}-{self._next_job_number()}"
            try:
                cursor = self.conn.execute(
                    """INSERT INTO jobs (customer_id, job_code, item, problem, quote, due_date, notes)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (customer_id, job_code, item, problem, quote, due_date, notes)
                )
                self.conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                continue
        raise Exception("Failed to generate unique job code after 10 attempts")
        
    def _next_job_number(self):
        today = datetime.now().strftime('%Y%m%d')
        cursor = self.conn.execute(
            "SELECT COUNT(*) as cnt FROM jobs WHERE job_code LIKE ?",
            (f"JOB-{today}-%",)
        )
        return cursor.fetchone()["cnt"] + 1
        
    def get_jobs(self, status=None):
        if status:
            return self.conn.execute(
                """SELECT j.*, c.name as customer_name, c.phone as customer_phone
                   FROM jobs j LEFT JOIN customers c ON j.customer_id = c.id
                   WHERE j.status = ? ORDER BY j.created_at DESC""",
                (status,)
            ).fetchall()
        return self.conn.execute(
            """SELECT j.*, c.name as customer_name, c.phone as customer_phone
               FROM jobs j LEFT JOIN customers c ON j.customer_id = c.id
               ORDER BY j.created_at DESC"""
        ).fetchall()
        
    def update_job_status(self, job_id, status):
        completed_at = datetime.now().isoformat() if status == "done" else None
        self.conn.execute(
            "UPDATE jobs SET status = ?, completed_at = ? WHERE id = ?",
            (status, completed_at, job_id)
        )
        self.conn.commit()
        
    def add_appointment(self, customer_id, date, time, purpose, notes=None):
        cursor = self.conn.execute(
            """INSERT INTO appointments (customer_id, date, time, purpose, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (customer_id, date, time, purpose, notes)
        )
        self.conn.commit()
        return cursor.lastrowid
        
    def get_appointments(self, date=None):
        if date:
            return self.conn.execute(
                """SELECT a.*, c.name as customer_name, c.phone as customer_phone
                   FROM appointments a LEFT JOIN customers c ON a.customer_id = c.id
                   WHERE a.date = ? ORDER BY a.time""",
                (date,)
            ).fetchall()
        return self.conn.execute(
            """SELECT a.*, c.name as customer_name, c.phone as customer_phone
               FROM appointments a LEFT JOIN customers c ON a.customer_id = c.id
               ORDER BY a.date, a.time"""
        ).fetchall()

    def search_appointments(self, query):
        q = f"%{query}%"
        return self.conn.execute(
            """SELECT a.*, c.name as customer_name, c.phone as customer_phone
               FROM appointments a LEFT JOIN customers c ON a.customer_id = c.id
               WHERE a.date LIKE ? OR a.purpose LIKE ? OR a.notes LIKE ? OR c.name LIKE ?
               ORDER BY a.date, a.time""",
            (q, q, q, q)
        ).fetchall()
        
    def add_invoice(self, job_id, amount, payment_method=None):
        for attempt in range(10):
            invoice_code = f"INV-{datetime.now().strftime('%Y%m%d')}-{self._next_invoice_number()}"
            try:
                cursor = self.conn.execute(
                    "INSERT INTO invoices (job_id, invoice_code, amount, payment_method) VALUES (?, ?, ?, ?)",
                    (job_id, invoice_code, amount, payment_method)
                )
                self.conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                continue
        raise Exception("Failed to generate unique invoice code after 10 attempts")
        
    def _next_invoice_number(self):
        today = datetime.now().strftime('%Y%m%d')
        cursor = self.conn.execute(
            "SELECT COUNT(*) as cnt FROM invoices WHERE invoice_code LIKE ?",
            (f"INV-{today}-%",)
        )
        return cursor.fetchone()["cnt"] + 1
        
    def mark_invoice_paid(self, invoice_id, payment_method):
        self.conn.execute(
            "UPDATE invoices SET paid = 1, payment_method = ? WHERE id = ?",
            (payment_method, invoice_id)
        )
        self.conn.commit()
        
    def get_invoices(self, paid=None):
        if paid is not None:
            return self.conn.execute(
                """SELECT i.*, j.item as job_item, c.name as customer_name
                   FROM invoices i
                   LEFT JOIN jobs j ON i.job_id = j.id
                   LEFT JOIN customers c ON j.customer_id = c.id
                   WHERE i.paid = ? ORDER BY i.created_at DESC""",
                (1 if paid else 0,)
            ).fetchall()
        return self.conn.execute(
            """SELECT i.*, j.item as job_item, c.name as customer_name
               FROM invoices i
               LEFT JOIN jobs j ON i.job_id = j.id
               LEFT JOIN customers c ON j.customer_id = c.id
               ORDER BY i.created_at DESC"""
        ).fetchall()
        
    def add_inventory_item(self, item_name, quantity=0, min_quantity=5, unit_price=0, notes=None):
        cursor = self.conn.execute(
            "INSERT INTO inventory (item_name, quantity, min_quantity, unit_price, notes) VALUES (?, ?, ?, ?, ?)",
            (item_name, quantity, min_quantity, unit_price, notes)
        )
        self.conn.commit()
        return cursor.lastrowid
        
    def get_inventory(self, search=None):
        if search:
            return self.conn.execute(
                "SELECT * FROM inventory WHERE item_name LIKE ? ORDER BY item_name",
                (f"%{search}%",)
            ).fetchall()
        return self.conn.execute("SELECT * FROM inventory ORDER BY item_name").fetchall()
        
    def get_inventory_item(self, item_id):
        return self.conn.execute(
            "SELECT * FROM inventory WHERE id = ?", (item_id,)
        ).fetchone()
        
    def update_inventory_item(self, item_id, item_name, quantity, min_quantity, unit_price, notes=None):
        self.conn.execute(
            "UPDATE inventory SET item_name=?, quantity=?, min_quantity=?, unit_price=?, notes=? WHERE id=?",
            (item_name, quantity, min_quantity, unit_price, notes, item_id)
        )
        self.conn.commit()
        
    def deduct_stock(self, item_id, amount):
        self.conn.execute(
            "UPDATE inventory SET quantity = quantity - ? WHERE id = ? AND quantity >= ?",
            (amount, item_id, amount)
        )
        self.conn.commit()
        
    def get_low_stock_items(self):
        return self.conn.execute(
            "SELECT * FROM inventory WHERE quantity <= min_quantity ORDER BY quantity"
        ).fetchall()
        
    def get_uncollected_jobs(self):
        return self.conn.execute("""
            SELECT j.*, c.name as customer_name, c.phone as customer_phone,
                   CAST((julianday('now') - julianday(j.completed_at)) AS INTEGER) as days_waiting
            FROM jobs j LEFT JOIN customers c ON j.customer_id = c.id
            WHERE j.status = 'done' AND j.completed_at IS NOT NULL
            AND CAST((julianday('now') - julianday(j.completed_at)) AS INTEGER) > 0
            ORDER BY j.completed_at ASC
        """).fetchall()

    def update_customer(self, cid, name, phone=None, email=None, address=None, notes=None):
        self.conn.execute("UPDATE customers SET name=?, phone=?, email=?, address=?, notes=? WHERE id=?",
                          (name, phone, email, address, notes, cid))
        self.conn.commit()

    def update_job(self, job_id, item=None, problem=None, quote=None, status=None, due_date=None, notes=None):
        self.conn.execute("UPDATE jobs SET item=?, problem=?, quote=?, status=?, due_date=?, notes=? WHERE id=?",
                          (item, problem, quote, status, due_date, notes, job_id))
        self.conn.commit()

    def update_appointment(self, apt_id, date=None, time=None, purpose=None, status=None, notes=None):
        self.conn.execute("UPDATE appointments SET date=?, time=?, purpose=?, status=?, notes=? WHERE id=?",
                          (date, time, purpose, status, notes, apt_id))
        self.conn.commit()

    def cleanup_old_invoices(self):
        """Delete paid invoices older than 7 days. Returns count of deleted invoices."""
        from datetime import timedelta
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor = self.conn.execute("DELETE FROM invoices WHERE paid=1 AND created_at < ?", (seven_days_ago,))
        self.conn.commit()
        return cursor.rowcount

    def close(self):
        self.conn.close()
