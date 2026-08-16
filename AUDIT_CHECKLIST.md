# Kerja Mudah - Audit Checklist

Production-readiness checklist for a registered business app.
Every item here is something that could cause data loss, lost sales, or a bad customer experience if it fails.

---

## Status Legend
- [x] PASS — verified working
- [ ] FAIL — needs fix before release
- [~] PARTIAL — works but has known gaps
- [-] N/A / Known limitation (acceptable for v1)

---

## 1. CRITICAL — Will Crash or Lose Data

### 1.1 Runtime Crashes
- [x] `sqlite3.Row` objects use bracket notation `row["key"]` everywhere (not `.get()`)
- [ ] **FAIL** Line 1595-1598: `send_pickup_reminder` — if `customer_phone` is None, phone becomes `"60"` (invalid), WhatsApp opens with no number
- [ ] **FAIL** Line 1682, 1829: `invs[-1]` crashes with `IndexError` if invoice list is empty
- [ ] **FAIL** Line 1688: `pdf_path` could be None from failed PDF generation, messagebox shows "None"
- [ ] **FAIL** Line 2264: Same `pdf_path` None issue in `download_inv_pdf`
- [x] All `webbrowser.open()` calls wrapped in try/except
- [x] All `os.startfile()` calls wrapped in try/except (except line 1922 — see 1.2)
- [ ] **FAIL** Line 1922: `os.startfile(pdf_path)` in `send_inv`/`send_email_inv` is NOT wrapped in try/except — crashes if file doesn't exist

### 1.2 Database Issues
- [x] All queries use parameterized statements (no SQL injection)
- [ ] **FAIL** No WAL mode — concurrent reads/writes can cause "database is locked" errors
- [ ] **FAIL** Line 137-143 (`database.py`): `_next_job_number()` race condition — two simultaneous jobs can get the same code, UNIQUE constraint throws unhandled exception
- [ ] **FAIL** Line 209-215 (`database.py`): Same race condition in `_next_invoice_number()`
- [ ] **FAIL** Line 307-313 (`database.py`): `cleanup_old_invoices()` deletes with no audit trail — data silently vanishes
- [x] Backup/restore works correctly
- [ ] **FAIL** No migration system — schema changes require manual SQL

### 1.3 Potential Data Loss
- [ ] **FAIL** No delete confirmation — if delete feature is ever added, must have confirmation
- [ ] **FAIL** No undo for any destructive operation
- [-] No way to delete records (actually prevents accidental loss — acceptable for v1)
- [-] `cleanup_old_invoices()` deletes paid invoices >7 days — user should be warned

---

## 2. HIGH — Broken Feature / Wrong Behavior

### 2.1 Search/Filter Bugs
- [ ] **FAIL** Line 1636: `_filter_jobs` compares against hardcoded `"search jobs..."` but placeholder is translated — if user types Malay/Chinese placeholder, filter returns no results
- [ ] **FAIL** Line 1980: Same bug in `_filter_custs` — hardcoded `"search customers..."`
- [ ] **FAIL** Line 2070: Same bug in `_filter_appts` — hardcoded `"search appointments..."`
- [ ] **FAIL** Line 2200: Same bug in `_filter_invs` — hardcoded `"search invoices..."`
- [ ] **FAIL** Line 2193: `_filter_invs()` called TWICE — unnecessary double render
- [x] Search trace race conditions fixed (trace after frame creation)

### 2.2 Scroll Issues
- [x] `pg_set()` has explicit scroll region update after rebuild
- [ ] **FAIL** `pg_home()` — no explicit scroll update after rebuilding content
- [ ] **FAIL** `pg_jobs()` — `_filter_jobs()` rebuilds without explicit scroll update
- [ ] **FAIL** `pg_custs()` — `_filter_custs()` rebuilds without explicit scroll update
- [ ] **FAIL** `pg_cal()` — `_filter_appts()` rebuilds without explicit scroll update
- [ ] **FAIL** `pg_invs()` — `_filter_invs()` rebuilds without explicit scroll update
- [x] `save_inv_fmt()` has explicit scroll update

### 2.3 Translation Gaps — UI Labels
- [ ] **FAIL** Line 2228: `text="WA"` button is hardcoded English abbreviation
- [ ] **FAIL** Line 1660: `j["status"].upper()` displays "PENDING"/"IN-PROGRESS"/"DONE" in English regardless of language
- [ ] **FAIL** Line 2630: Same status display issue in search results
- [ ] **FAIL** Line 2730: Settings edit fields use `"Name"`, `"Phone"`, `"Email"` as keys for `self.t()` — works but fragile
- [ ] **FAIL** Line 2924, 2955: `win.title(f"Edit {label}")` — "Edit" not translated in dialog titles
- [ ] **FAIL** Line 2511: Cleanup message hardcoded English
- [x] All search placeholders use `self.t()` keys
- [x] All page headers use `self.t()` keys
- [x] All button labels use `self.t()` keys
- [x] All error/success messages use `self.t()` keys

### 2.4 Translation Gaps — Customer-Facing Messages (WhatsApp/Email/PDF)
- [~] WhatsApp message templates are all English — customer sees English regardless of app language
- [~] Email subject/body templates are all English
- [~] PDF generation labels (Invoice:, Date:, Bill To:, Total:, etc.) are all English
- [~] Invoice preview shows hardcoded English demo data
- [x] Default business name fallback `"Shop"` is English — acceptable, user sets their own name
- [x] Default `"Thank you for your business!"` is English — user can change in settings
- [x] Default `"Payment due upon receipt"` is English — user can change in settings
- [x] Default `"INVOICE"` title is English — user can change in settings

### 2.5 Payment Methods
- [ ] **FAIL** Line 2250: Payment method color mapping uses hardcoded English keys (`"Cash"`, `"E-Wallet"`, etc.)
- [ ] **FAIL** Line 2521: Payment method radio buttons use hardcoded English labels
- [ ] **FAIL** DB stores English strings — if user switches language, existing payment methods don't translate

---

## 3. MEDIUM — Security / Best Practice

### 3.1 Security
- [ ] **FAIL** PIN is `SHA256(pin)` with no salt — only 10,000 possible PINs, trivially brute-forced
- [ ] **FAIL** License key is `SHA256(HWID)[:20]` — trivially reversible
- [ ] **FAIL** HWID is computed from `platform.node()`, `platform.processor()`, `uuid.getnode()` — all spoofable
- [ ] **FAIL** Line 2496: Exception details shown to user via `f"Failed to generate PDF:\n{str(e)}"` — could leak file paths
- [ ] **FAIL** Line 2684: Backup error shows raw exception: `f": {e}"`
- [ ] **FAIL** Line 2702: Restore error shows raw exception: `f": {e}"`
- [ ] **FAIL** Line 2721: Export error shows raw exception: `str(e)`
- [x] No secrets in source code
- [x] No sensitive data in error messages (except above exceptions)
- [x] `.gitignore` excludes `keygen.py`, `SALES_CHEAT_SHEET.txt`, `data/`, `dist/`, `build/`, `*.spec`, `*.db`

### 3.2 Error Handling
- [ ] **FAIL** Line 9 (`database.py`): `sqlite3.connect()` has no try/except — crashes if DB path is invalid or locked
- [ ] **FAIL** Line 90 (`database.py`): `self.conn.commit()` has no try/except
- [x] All `webbrowser.open()` calls wrapped in try/except
- [~] All `os.startfile()` calls wrapped — except line 1922
- [x] All messagebox calls use safe strings
- [ ] **FAIL** Line 3022-3023: `rm_pin()` bypasses Database class API, executes SQL directly on `self.db.conn`

### 3.3 Thread Safety
- [ ] **FAIL** Single `sqlite3.Connection` shared across all operations — not thread-safe by default
- [ ] **FAIL** No explicit `isolation_level` set on connection
- [x] App is single-threaded (Tkinter mainloop) — reduces risk but doesn't eliminate it

---

## 4. LOW — UX Polish / Performance

### 4.1 Input Validation
- [x] `field()` validates max_len on general text fields
- [x] `name_field()` blocks `<>{}[]|\"'` and enforces max 50 chars
- [x] `phone_field()` allows only digits/`+-` and enforces max 20 chars
- [x] `email_field()` blocks `<>{}[]|\` and enforces max 80 chars
- [x] `pin_field()` enforces 4 digits only
- [x] `number_field()` allows only digits/`.-` and enforces max 12 chars
- [x] `date_field()` enforces month 1-12, day 1-31
- [ ] **FAIL** `text_area_field()` validates max_len but does NOT filter dangerous characters
- [ ] **FAIL** Line 1726-1730: Phone field in `pg_new_job` has NO length limit (unlike `phone_field()`)
- [ ] **FAIL** Line 1734-1735: Email field in `pg_new_job` has NO validation
- [ ] **FAIL** Line 2111-2116: `edit_appt` date field is raw Entry — no validation, no date picker
- [ ] **FAIL** Line 2931-2932: `_show_biz_edit_dialog` uses raw Entry — no validation
- [ ] **FAIL** Line 2960-2961: `_edit_invoice_param` uses raw Entry — no validation
- [x] Required fields enforced: customer name, item, date

### 4.2 Performance
- [ ] **FAIL** Line 1541-1544: `pg_home` loads ALL jobs, appointments, invoices for dashboard
- [ ] **FAIL** Line 1634: `_filter_jobs()` loads ALL jobs, filters in Python — should use SQL WHERE
- [ ] **FAIL** Line 1978: `_filter_custs()` loads ALL customers, filters in Python
- [ ] **FAIL** Line 2198: `_filter_invs()` loads ALL invoices, filters in Python
- [ ] **FAIL** Line 2546-2553: `pg_rpt()` loads ALL jobs and invoices for summary stats
- [ ] **FAIL** Line 2613-2619: `do_search()` loads ALL records from ALL tables into memory
- [ ] **FAIL** Line 1666-1667: Inside jobs table loop, `get_invoices()` called for EVERY done row — should be called once before loop
- [ ] **FAIL** Line 2256: `download_inv_pdf` iterates all jobs to find one by job_id — should use direct query
- [ ] Missing database indexes on frequently queried columns: `jobs.status`, `jobs.customer_id`, `invoices.job_id`, `invoices.paid`, `appointments.date`

### 4.3 UI Consistency
- [x] Sidebar dark theme consistent across all pages
- [x] Content area scrollable on all pages
- [x] Demo mode banner fixed at top
- [x] Minimum window size enforced (900x650)
- [x] Window resize doesn't break layout
- [x] Table system uses consistent grid layout with cell() helper
- [x] All tables have alternating row colors
- [x] All tables have no borders (clean look)
- [x] Headers align with data columns
- [x] Long text truncates with "..." and shows full text on hover
- [x] Action buttons always visible on far right
- [x] Status badges with colored backgrounds
- [ ] Mixed font sizes for same-purpose elements (report cards use 9/14/8, tables use 10/11)
- [ ] Mixed padding values across pages (padx=10, 12, 20, 25, 28)
- [ ] Cancel buttons inconsistent styling (some use tk.Button directly, some use self.btn())

### 4.4 Feature Completeness
- [x] Setup wizard with language selection
- [x] PIN login with SHA-256 hash
- [x] License activation with HWID
- [x] Demo mode (7-day, 10-job limit)
- [x] Dashboard with stats cards, reminders, quick actions
- [x] Jobs: create, list, edit, mark done, search/filter
- [x] Customers: create, list, edit, search/filter
- [x] Appointments: create, list, edit, search/filter
- [x] Invoices: create from job, mark paid, search/filter
- [x] Invoice PDF generation (fpdf)
- [x] Invoice preview with customizable format
- [x] WhatsApp integration (opens wa.me links)
- [x] Email integration (opens mailto: links)
- [x] Google review link in messages
- [x] Reports page with revenue stats
- [x] Backup/restore (SQLite file copy)
- [x] CSV export (customers, jobs, invoices)
- [x] Settings: business info, PIN, language, invoice format, startup, invoice parameters
- [x] Auto-startup (creates .bat in Windows Startup folder)
- [x] Language switching (EN/MS/ZH)
- [x] Date picker with calendar widget
- [x] Global search (jobs, customers, invoices)
- [x] Pickup reminders via WhatsApp
- [x] Invoice cleanup (paid invoices >7 days)
- [-] No delete records (prevents accidental loss — acceptable for v1)
- [-] No undo (acceptable for v1)
- [-] No customer detail view (shows all jobs/invoices for one customer)
- [-] No address field in customer form (schema exists but no UI)

---

## 5. BUILD & DISTRIBUTION

- [x] PyInstaller builds successfully (`python -m PyInstaller --onefile --windowed`)
- [x] `.exe` runs on clean Windows install
- [x] All dependencies bundled (tkinter, sqlite3, fpdf, PIL, webbrowser)
- [x] `.gitignore` excludes sensitive files
- [x] No secrets in repository
- [x] Database file (`data/data.db`) included in `dist/` for demo
- [x] GitHub repo private at `https://github.com/laizhengian/kerja-mudah`

---

## 6. TRANSLATION COMPLETENESS

### 6.1 Key Coverage (per language)
- English (`en`): ~327 keys
- Malay (`ms`): ~327 keys
- Chinese (`zh`): ~327 keys

### 6.2 Categories by Translation Status
- [x] **Fully translated:** All UI labels, buttons, headers, error messages, success messages, search placeholders, settings labels, report labels, dashboard labels
- [~] **Partially translated:** Payment method names (UI labels translated, but DB stores English)
- [ ] **Not translated:** WhatsApp message templates, email templates, PDF generation labels, invoice preview demo data, status badges in jobs table, "WA" button, cleanup messages

---

## 7. KNOWN LIMITATIONS (Acceptable for v1)

1. Customer-facing messages (WhatsApp, email, PDF) are English-only — translating requires reworking message composition
2. No delete records — prevents accidental loss
3. No undo — acceptable for v1
4. No customer detail view — can be added later
5. Address field exists in DB but no UI — can be added later
6. PIN is not salted — acceptable for local desktop app (not networked)
7. License key is weak — acceptable for small business (not enterprise DRM)
8. All filtering is in-memory — acceptable for datasets under ~10,000 records
9. No migration system — acceptable for v1 (schema is stable)

---

*Last updated: 16 August 2026*
*Audited by: AI assistant (comprehensive line-by-line review of main.py and database.py)*
