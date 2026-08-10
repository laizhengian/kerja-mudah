import tkinter as tk
from tkinter import ttk, messagebox
import os, sys, hashlib, webbrowser, urllib.parse, platform, uuid
from datetime import datetime, timedelta
from fpdf import FPDF

APP_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
os.chdir(APP_DIR)
from database import Database

def get_hwid():
    raw = f"{platform.node()}-{platform.processor()}-{uuid.getnode()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def check_license(db):
    hwid = db.get_setting("licensed_hwid")
    key = db.get_setting("license_key")
    if hwid and key:
        expected = hashlib.sha256(hwid.encode()).hexdigest()[:20].upper()
        if key.upper() == expected:
            return True
    return False

def is_demo(db):
    if check_license(db):
        return False
    install_date = db.get_setting("install_date")
    if not install_date:
        db.set_setting("install_date", datetime.now().isoformat())
        install_date = datetime.now().isoformat()
    try:
        days = (datetime.now() - datetime.fromisoformat(install_date)).days
    except:
        days = 0
    return days <= 7

C = {
    "bg": "#FFFFFF", "side": "#111111", "side_h": "#1E1E1E",
    "card": "#F5F5F5", "card_h": "#EBEBEB", "bdr": "#E0E0E0",
    "txt": "#111111", "txt2": "#555555", "txt3": "#999999",
    "pri": "#111111", "pri_h": "#2A2A2A",
    "ok": "#16A34A", "warn": "#D97706", "err": "#DC2626",
    "white": "#FFFFFF",
}

T = {
    "en": {
        "app_title": "Kerja Mudah",
        "home": "Home", "jobs": "Jobs", "customers": "Customers",
        "appointments": "Appointments", "invoices": "Invoices",
        "reports": "Reports", "search": "Search", "backup": "Backup", "settings": "Settings",
        "dashboard": "Dashboard", "active_jobs": "Active Jobs", "today": "Today",
        "outstanding": "Outstanding", "jobs_done": "Jobs Done",
        "reminders": "Reminders", "quick_actions": "Quick Actions",
        "new_job": "+ New Job", "new_customer": "+ Customer", "new_appointment": "+ Appointment",
        "new_job_title": "New Job", "new_customer_title": "New Customer", "new_appointment_title": "New Appointment",
        "customer": "Customer", "phone": "Phone", "item": "Item",
        "problem": "Service / Problem Details", "quote": "Quote (RM)", "email": "Email", "notes": "Notes",
        "due_date": "Due Date", "date": "Date", "time": "Time",
        "purpose": "Purpose", "save": "Save", "cancel": "Cancel",
        "create_invoice": "Create Invoice", "from_job": "+ From Job",
        "unpaid": "Unpaid", "paid": "Paid", "mark_paid": "Mark Paid",
        "send_whatsapp": "Send WhatsApp", "how_paid": "How did they pay?",
        "cash": "Cash", "e_wallet": "E-Wallet", "card": "Card", "transfer": "Transfer",
        "job_complete": "Job Complete!", "invoice_whatsapp": "Invoice + WhatsApp",
        "just_invoice": "Just Invoice", "skip": "Skip",
        "no_jobs": "No jobs yet", "no_customers": "No customers yet",
        "no_appointments": "No appointments today", "no_invoices": "No invoices yet",
        "no_results": "No results for", "type_search": "Type and press Search",
        "results_for": "result(s) for", "export_csv": "Export to CSV",
        "business_info": "Business Info", "name": "Name", "security": "Security",
        "pin_active": "PIN: Active", "pin_not_set": "PIN: Not Set",
        "set_pin": "Set PIN", "change_pin": "Change PIN", "remove_pin": "Remove PIN",
        "enter_pin": "Enter PIN", "login": "Login", "wrong_pin": "Wrong PIN",
        "welcome": "Welcome", "setup_title": "Set up in 1 minute",
        "business_name": "Business Name", "get_started": "Get Started",
        "offline_msg": "Your data stays on this computer. No internet required.",
        "error": "Error", "done": "Done", "warning": "Warning",
        "today_appointments": "Today's Appointments",
        "unpaid_invoices": "unpaid invoice(s)",
        "confirm_pin": "Confirm PIN",
        "service_details": "Service / Problem Details",
        "google_review": "Google Review Link",
        "google_review_hint": "e.g. https://g.page/r/ABC123/review",
        "leave_review": "We'd love your feedback!",
        "rate_us": "Leave us a Google review",
    },
    "ms": {
        "app_title": "Kerja Mudah",
        "home": "Utama", "jobs": "Kerja", "customers": "Pelanggan",
        "appointments": "Temujanji", "invoices": "Invois",
        "reports": "Laporan", "search": "Carian", "backup": "Sandaran", "settings": "Tetapan",
        "dashboard": "Papan Pemuka", "active_jobs": "Kerja Aktif", "today": "Hari Ini",
        "outstanding": "Belum Dibayar", "jobs_done": "Kerja Selesai",
        "reminders": "Peringatan", "quick_actions": "Tindakan Pantas",
        "new_job": "+ Kerja Baru", "new_customer": "+ Pelanggan", "new_appointment": "+ Temujanji",
        "new_job_title": "Kerja Baru", "new_customer_title": "Pelanggan Baru", "new_appointment_title": "Temujanji Baru",
        "customer": "Pelanggan", "phone": "Telefon", "item": "Barang",
        "problem": "Perkhidmatan / Butiran Masalah", "quote": "Sebut Harga (RM)", "email": "Emel", "notes": "Nota",
        "due_date": "Tarikh Akhir", "date": "Tarikh", "time": "Masa",
        "purpose": "Tujuan", "save": "Simpan", "cancel": "Batal",
        "create_invoice": "Cipta Invois", "from_job": "+ Dari Kerja",
        "unpaid": "Belum Dibayar", "paid": "Dibayar", "mark_paid": "Tanda Dibayar",
        "send_whatsapp": "Hantar WhatsApp", "how_paid": "Bayar guna apa?",
        "cash": "Tunai", "e_wallet": "E-Wallet", "card": "Kad", "transfer": "Pemindahan",
        "job_complete": "Kerja Selesai!", "invoice_whatsapp": "Invois + WhatsApp",
        "just_invoice": "Invois Sahaja", "skip": "Langkau",
        "no_jobs": "Tiada kerja lagi", "no_customers": "Tiada pelanggan lagi",
        "no_appointments": "Tiada temujanji hari ini", "no_invoices": "Tiada invois lagi",
        "no_results": "Tiada hasil untuk", "type_search": "Taip dan tekan Cari",
        "results_for": "hasil untuk", "export_csv": "Eksport ke CSV",
        "business_info": "Maklumat Perniagaan", "name": "Nama", "security": "Keselamatan",
        "pin_active": "PIN: Aktif", "pin_not_set": "PIN: Belum ditetapkan",
        "set_pin": "Tetapkan PIN", "change_pin": "Tukar PIN", "remove_pin": "Buang PIN",
        "enter_pin": "Masukkan PIN", "login": "Log Masuk", "wrong_pin": "PIN salah",
        "welcome": "Selamat Datang", "setup_title": "Persediaan dalam 1 minit",
        "business_name": "Nama Perniagaan", "get_started": "Mula",
        "offline_msg": "Data anda kekal di komputer ini. Internet tidak diperlukan.",
        "error": "Ralat", "done": "Selesai", "warning": "Amaran",
        "today_appointments": "Temujanji Hari Ini",
        "unpaid_invoices": "invois belum dibayar",
        "confirm_pin": "Sahkan PIN",
        "service_details": "Perkhidmatan / Butiran Masalah",
        "google_review": "Pautan Google Review",
        "google_review_hint": "cth. https://g.page/r/ABC123/review",
        "leave_review": "Kami menghargai maklum balas anda!",
        "rate_us": "Tinggalkan Google review untuk kami",
    },
    "zh": {
        "app_title": "Kerja Mudah",
        "home": "主页", "jobs": "工作", "customers": "客户",
        "appointments": "预约", "invoices": "发票",
        "reports": "报告", "search": "搜索", "backup": "备份", "settings": "设置",
        "dashboard": "仪表板", "active_jobs": "进行中", "today": "今天",
        "outstanding": "未收款", "jobs_done": "已完成",
        "reminders": "提醒", "quick_actions": "快捷操作",
        "new_job": "+ 新工作", "new_customer": "+ 客户", "new_appointment": "+ 预约",
        "new_job_title": "新工作", "new_customer_title": "新客户", "new_appointment_title": "新预约",
        "customer": "客户", "phone": "电话", "item": "物品",
        "problem": "服务/问题详情", "quote": "报价 (RM)", "email": "电邮", "notes": "备注",
        "due_date": "截止日期", "date": "日期", "time": "时间",
        "purpose": "目的", "save": "保存", "cancel": "取消",
        "create_invoice": "创建发票", "from_job": "+ 从工作",
        "unpaid": "未付款", "paid": "已付款", "mark_paid": "标记已付",
        "send_whatsapp": "发送WhatsApp", "how_paid": "如何付款？",
        "cash": "现金", "e_wallet": "电子钱包", "card": "银行卡", "transfer": "转账",
        "job_complete": "工作完成！", "invoice_whatsapp": "发票 + WhatsApp",
        "just_invoice": "仅发票", "skip": "跳过",
        "no_jobs": "暂无工作", "no_customers": "暂无客户",
        "no_appointments": "今天没有预约", "no_invoices": "暂无发票",
        "no_results": "未找到", "type_search": "输入后点击搜索",
        "results_for": "个结果", "export_csv": "导出CSV",
        "business_info": "商家信息", "name": "姓名", "security": "安全",
        "pin_active": "PIN: 已启用", "pin_not_set": "PIN: 未设置",
        "set_pin": "设置PIN", "change_pin": "修改PIN", "remove_pin": "删除PIN",
        "enter_pin": "输入PIN", "login": "登录", "wrong_pin": "PIN错误",
        "welcome": "欢迎", "setup_title": "1分钟完成设置",
        "business_name": "商家名称", "get_started": "开始",
        "offline_msg": "数据保存在本电脑，无需网络。",
        "error": "错误", "done": "完成", "warning": "警告",
        "today_appointments": "今日预约",
        "unpaid_invoices": "张未付款发票",
        "confirm_pin": "确认PIN",
        "service_details": "服务/问题详情",
        "google_review": "Google评价链接",
        "google_review_hint": "例如 https://g.page/r/ABC123/review",
        "leave_review": "我们期待您的反馈！",
        "rate_us": "请给我们留个Google评价",
    },
}

def tr(lang, key):
    return T.get(lang, T["en"]).get(key, T["en"].get(key, key))

class App:
    def __init__(self):
        self.db = Database(os.path.join(APP_DIR, "data", "data.db"))
        self.db.cleanup_old_invoices()
        self.lang = self.db.get_setting("language", "en")
        self.root = tk.Tk()
        self.root.title(tr(self.lang, "app_title"))
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        self.root.configure(bg=C["bg"])
        try:
            self.root.iconbitmap(default="")
        except:
            pass
        if check_license(self.db):
            if not self.db.get_setting("setup_complete"):
                self.wizard()
            elif self.db.get_setting("pin_hash"):
                self.pin_screen()
            else:
                self.layout()
        else:
            self.activate_screen()

    def fmt_date(self, date_str):
        if not date_str:
            return "-"
        try:
            dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
            return dt.strftime("%d %B %Y")
        except:
            try:
                dt = datetime.strptime(date_str, "%d/%m/%Y")
                return dt.strftime("%d %B %Y")
            except:
                return date_str

    def h(self, p):
        return hashlib.sha256(p.encode()).hexdigest()

    def t(self, key):
        lang = self.lang.get() if isinstance(self.lang, tk.StringVar) else self.lang
        return tr(lang, key)

    def is_demo(self):
        return is_demo(self.db)

    def is_licensed(self):
        return check_license(self.db)

    def clr(self):
        if hasattr(self, 'content') and self.content:
            for w in self.content.winfo_children():
                w.destroy()
        if hasattr(self, 'content_canvas'):
            self.content_canvas.yview_moveto(0)

    def hdr(self, t, btn=None, cmd=None):
        f = tk.Frame(self.content, bg=C["bg"], padx=28, pady=22)
        f.pack(fill="x")
        tk.Label(f, text=t, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 22, "bold")).pack(side="left")
        if btn:
            b = tk.Button(f, text=btn, command=cmd, bg=C["pri"], fg=C["white"], font=("Segoe UI", 11, "bold"), bd=0, padx=20, pady=10, cursor="hand2")
            b.pack(side="right")
            b.bind("<Enter>", lambda e: b.configure(bg=C["pri_h"]))
            b.bind("<Leave>", lambda e: b.configure(bg=C["pri"]))

    def row(self, parent, **kw):
        f = tk.Frame(parent, bg=C["card"], bd=1, relief="solid", pady=14, padx=20)
        f.pack(fill="x", pady=4, **kw)
        return f

    def btn(self, parent, txt, cmd, bg=None, fg=None):
        b = tk.Button(parent, text=txt, command=cmd, bg=bg or C["pri"], fg=fg or C["white"], font=("Segoe UI", 11, "bold"), bd=0, padx=20, pady=10, cursor="hand2")
        b.bind("<Enter>", lambda e: b.configure(bg=C["pri_h"] if bg == C["pri"] or not bg else bg))
        b.bind("<Leave>", lambda e: b.configure(bg=bg or C["pri"]))
        return b

    def field(self, parent, label, default=""):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        e = tk.Entry(f, font=("Segoe UI", 12), bd=1, relief="solid")
        if default:
            e.insert(0, default)
        e.pack(side="left", fill="x", expand=True, ipady=6)
        return e

    def date_field(self, parent, label, default=None):
        import calendar
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        today = datetime.now() if not default else datetime.strptime(default, "%Y-%m-%d")
        var = tk.StringVar(value=today.strftime("%Y-%m-%d"))
        frame = tk.Frame(f, bg=C["bg"])
        frame.pack(side="left")
        entry = tk.Entry(frame, textvariable=var, font=("Segoe UI", 12), bd=1, relief="solid", width=12)
        entry.pack(side="left")
        def show_cal():
            win = tk.Toplevel(self.root)
            win.title("Pick Date")
            win.geometry("280x320")
            win.configure(bg=C["bg"])
            win.grab_set()
            try:
                current = datetime.strptime(var.get(), "%Y-%m-%d")
            except:
                current = datetime.now()
            month_var = tk.StringVar(value=current.strftime("%B %Y"))
            def change_month(delta):
                nonlocal current
                current = current.replace(day=1) + timedelta(days=32*delta)
                current = current.replace(day=1)
                month_var.set(current.strftime("%B %Y"))
                draw_calendar()
            def draw_calendar():
                for w in cal_frame.winfo_children():
                    w.destroy()
                hdr = tk.Frame(cal_frame, bg=C["bg"])
                hdr.pack(fill="x", pady=5)
                tk.Button(hdr, text="<", command=lambda: change_month(-1), bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold"), bd=0, padx=8, cursor="hand2").pack(side="left")
                tk.Label(hdr, textvariable=month_var, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold")).pack(side="left", expand=True)
                tk.Button(hdr, text=">", command=lambda: change_month(1), bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold"), bd=0, padx=8, cursor="hand2").pack(side="right")
                days_frame = tk.Frame(cal_frame, bg=C["bg"])
                days_frame.pack(fill="x")
                for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
                    tk.Label(days_frame, text=d, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 9, "bold"), width=4).pack(side="left")
                cal = calendar.monthcalendar(current.year, current.month)
                for week in cal:
                    week_frame = tk.Frame(cal_frame, bg=C["bg"])
                    week_frame.pack(fill="x")
                    for day in week:
                        if day == 0:
                            tk.Label(week_frame, text="", bg=C["bg"], width=4).pack(side="left")
                        else:
                            day_str = f"{current.year}-{current.month:02d}-{day:02d}"
                            is_today = day_str == datetime.now().strftime("%Y-%m-%d")
                            is_selected = day_str == var.get()
                            bg = C["pri"] if is_selected else (C["card"] if is_today else C["bg"])
                            fg = C["white"] if is_selected else C["txt"]
                            b = tk.Button(week_frame, text=str(day), bg=bg, fg=fg, font=("Segoe UI", 10, "bold" if is_today else ""), bd=0, width=4, cursor="hand2", command=lambda d=day_str, w=win: [var.set(d), w.destroy()])
                            b.pack(side="left")
                tk.Button(cal_frame, text="Today", command=lambda: [var.set(datetime.now().strftime("%Y-%m-%d")), win.destroy()], bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10), bd=1, relief="solid", padx=15, pady=5, cursor="hand2").pack(pady=10)
            cal_frame = tk.Frame(win, bg=C["bg"])
            cal_frame.pack(fill="both", expand=True, padx=10, pady=10)
            draw_calendar()
        tk.Button(frame, text="Pick", command=show_cal, bg=C["card"], fg=C["txt"], font=("Segoe UI", 10), bd=1, relief="solid", padx=8, cursor="hand2").pack(side="left", padx=5)
        return var

    def time_field(self, parent, label, default=None):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        now = datetime.now() if not default else datetime.strptime(default, "%H:%M")
        hour_var = tk.StringVar(value=str(now.hour).zfill(2))
        min_var = tk.StringVar(value=str(now.minute // 15 * 15).zfill(2))
        frame = tk.Frame(f, bg=C["bg"])
        frame.pack(side="left")
        hours = [str(i).zfill(2) for i in range(24)]
        h_menu = tk.OptionMenu(frame, hour_var, *hours)
        h_menu.configure(font=("Segoe UI", 11), width=3, bg=C["white"])
        h_menu.pack(side="left")
        tk.Label(frame, text=":", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 14, "bold")).pack(side="left", padx=4)
        mins = ["00", "15", "30", "45"]
        m_menu = tk.OptionMenu(frame, min_var, *mins)
        m_menu.configure(font=("Segoe UI", 11), width=3, bg=C["white"])
        m_menu.pack(side="left")
        return hour_var, min_var

    def wizard(self):
        self.clr()
        self.root.configure(bg=C["bg"])
        c = tk.Frame(self.root, bg=C["bg"])
        c.pack(expand=True, fill="both")
        tk.Label(c, text=self.t("welcome"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 28, "bold")).pack(pady=8)
        tk.Label(c, text=self.t("setup_title"), bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 13)).pack(pady=8)
        f = tk.Frame(c, bg=C["bg"]); f.pack()
        self.se = {}
        for l, d in [("Business Name", ""), ("Phone", "+60"), ("Email", "")]:
            self.se[l] = self.field(f, self.t(l.lower().replace(" ","_")), d)
        gf = tk.Frame(f, bg=C["bg"]); gf.pack(fill="x", pady=8)
        tk.Label(gf, text=self.t("google_review"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        self.se["Google Review"] = tk.Entry(gf, font=("Segoe UI", 12), bd=1, relief="solid")
        self.se["Google Review"].pack(side="left", fill="x", expand=True, ipady=6)
        tk.Label(gf, text=self.t("google_review_hint"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 9)).pack(side="left", padx=8)
        lf = tk.Frame(f, bg=C["bg"]); lf.pack(fill="x", pady=12)
        tk.Label(lf, text="Language", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        self.lang = tk.StringVar(value="en")
        for v, t in [("en","English"),("ms","Bahasa Malaysia"),("zh","Chinese")]:
            tk.Radiobutton(lf, text=t, variable=self.lang, value=v, bg=C["bg"], font=("Segoe UI", 11)).pack(side="left", padx=8)
        self.btn(c, self.t("get_started"), self.save_wizard).pack(pady=30)
        tk.Label(c, text=self.t("offline_msg"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack()

    def save_wizard(self):
        n = self.se["Business Name"].get().strip()
        if not n:
            return messagebox.showerror("Error", "Enter business name")
        self.db.set_setting("business_name", n)
        self.db.set_setting("business_phone", self.se["Phone"].get().strip())
        self.db.set_setting("business_email", self.se["Email"].get().strip())
        self.db.set_setting("google_review", self.se["Google Review"].get().strip())
        self.db.set_setting("language", self.lang.get())
        self.db.set_setting("setup_complete", "true")
        self.layout()

    def pin_screen(self):
        self.clr()
        self.root.configure(bg=C["bg"])
        c = tk.Frame(self.root, bg=C["bg"]); c.pack(expand=True, fill="both")
        n = self.db.get_setting("business_name", "Shop")
        tk.Label(c, text=n, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 26, "bold")).pack(pady=8)
        tk.Label(c, text=self.t("enter_pin"), bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 12)).pack(pady=8)
        self.pin_e = tk.Entry(c, font=("Segoe UI", 24), bd=1, relief="solid", width=8, justify="center", show="*")
        self.pin_e.pack(ipady=8)
        self.pin_e.focus()
        self.pin_e.bind("<Return>", lambda e: self.chk_pin())
        self.btn(c, self.t("login"), self.chk_pin).pack(pady=20)

    def chk_pin(self):
        if self.h(self.pin_e.get().strip()) == self.db.get_setting("pin_hash"):
            self.layout()
        else:
            messagebox.showerror(self.t("error"), self.t("wrong_pin"))
            self.pin_e.delete(0, tk.END)

    def activate_screen(self):
        self.clr()
        self.root.configure(bg=C["bg"])
        c = tk.Frame(self.root, bg=C["bg"])
        c.pack(expand=True, fill="both")
        hwid = get_hwid()
        tk.Label(c, text="License Activation Required", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 24, "bold")).pack(pady=8)
        tk.Label(c, text="Enter your license key to activate", bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 12)).pack(pady=5)
        hwid_frame = tk.Frame(c, bg=C["card"], bd=1, relief="solid", padx=15, pady=10)
        hwid_frame.pack(pady=15, padx=40, fill="x")
        tk.Label(hwid_frame, text="Your Hardware ID (send this to get a key):", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w")
        hwid_row = tk.Frame(hwid_frame, bg=C["card"])
        hwid_row.pack(fill="x", pady=5)
        tk.Label(hwid_row, text=hwid, bg=C["card"], fg=C["pri"], font=("Consolas", 16, "bold")).pack(side="left")
        def copy_hwid():
            self.root.clipboard_clear()
            self.root.clipboard_append(hwid)
            messagebox.showinfo("Copied", "HWID copied to clipboard!")
        copy_btn = tk.Button(hwid_row, text="Copy", command=copy_hwid, bg=C["pri"], fg=C["white"], font=("Segoe UI", 10, "bold"), bd=0, padx=12, pady=4, cursor="hand2")
        copy_btn.pack(side="right")
        copy_btn.bind("<Enter>", lambda e: copy_btn.configure(bg=C["pri_h"]))
        copy_btn.bind("<Leave>", lambda e: copy_btn.configure(bg=C["pri"]))
        self.key_entry = tk.Entry(c, font=("Segoe UI", 14), bd=1, relief="solid", width=30, justify="center")
        self.key_entry.pack(pady=15, ipady=8)
        bf = tk.Frame(c, bg=C["bg"])
        bf.pack(pady=10)
        def activate():
            key = self.key_entry.get().strip()
            expected = hashlib.sha256(hwid.encode()).hexdigest()[:20].upper()
            if key.upper() == expected:
                self.db.set_setting("licensed_hwid", hwid)
                self.db.set_setting("license_key", key)
                for w in self.root.winfo_children():
                    w.destroy()
                messagebox.showinfo("Activated", "License activated! You can now use the full app.")
                if not self.db.get_setting("setup_complete"):
                    self.wizard()
                else:
                    self.layout()
            else:
                messagebox.showerror("Invalid Key", "This license key is not valid.")
        def try_demo():
            for w in self.root.winfo_children():
                w.destroy()
            if not self.db.get_setting("setup_complete"):
                self.wizard()
            else:
                self.layout()
        b = tk.Button(bf, text="Activate", command=activate, bg=C["pri"], fg=C["white"], font=("Segoe UI", 12, "bold"), bd=0, padx=30, pady=10, cursor="hand2")
        b.pack(side="left", padx=5)
        b.bind("<Enter>", lambda e: b.configure(bg=C["pri_h"]))
        b.bind("<Leave>", lambda e: b.configure(bg=C["pri"]))
        b2 = tk.Button(bf, text="Try Demo (7 days)", command=try_demo, bg=C["card"], fg=C["txt"], font=("Segoe UI", 12), bd=1, relief="solid", padx=20, pady=10, cursor="hand2")
        b2.pack(side="left", padx=5)
        tk.Label(c, text="Demo mode: limited to 10 jobs, 7 day trial", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack(pady=10)
        tk.Label(c, text="Contact seller to get your license key", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack()

    def layout(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=C["bg"])
        self.root.title(self.t("app_title"))
        self.side = tk.Frame(self.root, bg=C["side"], width=240)
        self.side.pack(side="left", fill="y")
        self.side.pack_propagate(False)
        main_frame = tk.Frame(self.root, bg=C["bg"])
        main_frame.pack(side="left", fill="both", expand=True)
        self.content_canvas = tk.Canvas(main_frame, bg=C["bg"], highlightthickness=0)
        self.content_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.content_canvas.yview)
        self.content = tk.Frame(self.content_canvas, bg=C["bg"])
        self.content.bind("<Configure>", lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))
        self.content_canvas.create_window((0, 0), window=self.content, anchor="nw", tags="inner")
        self.content_canvas.configure(yscrollcommand=self.content_scrollbar.set)
        self.content_scrollbar.pack(side="right", fill="y")
        self.content_canvas.pack(side="left", fill="both", expand=True)
        self.content_canvas.bind("<Configure>", lambda e: self.content_canvas.itemconfig("inner", width=e.width))
        def _on_mousewheel(event):
            self.content_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.content_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        if self.is_demo():
            days_left = 7
            try:
                install_date = self.db.get_setting("install_date")
                if install_date:
                    days_left = 7 - (datetime.now() - datetime.fromisoformat(install_date)).days
            except:
                pass
            demo_bar = tk.Frame(self.root, bg="#FEF3C7", height=30)
            demo_bar.place(relx=0.5, rely=0, anchor="n", relwidth=1)
            demo_bar.pack_propagate(False)
            tk.Label(demo_bar, text=f"DEMO MODE - {days_left} days remaining | Activate with license key", bg="#FEF3C7", fg="#92400E", font=("Segoe UI", 10, "bold")).pack(expand=True)
        n = self.db.get_setting("business_name", "Shop")
        tk.Label(self.side, text=n, bg=C["side"], fg=C["white"], font=("Segoe UI", 15, "bold"), pady=25, wraplength=220).pack(fill="x")
        tk.Frame(self.side, bg="#2A2A2A", height=1).pack(fill="x", padx=20)
        for txt, cmd in [("Home", self.pg_home), ("Jobs", self.pg_jobs), ("Customers", self.pg_custs),
                         ("Appointments", self.pg_cal), ("Invoices", self.pg_invs), ("Reports", self.pg_rpt),
                         ("Search", self.pg_search), ("Backup", self.pg_backup), ("Settings", self.pg_set)]:
            b = tk.Button(self.side, text=f"  {self.t(txt.lower())}", command=cmd, bg=C["side"], fg="#AAAAAA", font=("Segoe UI", 12), bd=0, anchor="w", padx=25, pady=14, activebackground=C["side_h"], activeforeground=C["white"], cursor="hand2")
            b.pack(fill="x")
            b.bind("<Enter>", lambda e, b=b: b.configure(bg=C["side_h"], fg=C["white"]))
            b.bind("<Leave>", lambda e, b=b: b.configure(bg=C["side"], fg="#AAAAAA"))
        self.pg_home()

    def pg_home(self):
        self.clr()
        self.hdr(self.t("dashboard"))
        today = datetime.now().strftime("%Y-%m-%d")
        jobs = self.db.get_jobs()
        active = len([j for j in jobs if j["status"] != "done"])
        appts = len(self.db.get_appointments(today))
        unpaid = self.db.get_invoices(paid=False)
        owed = sum(i["amount"] for i in unpaid)
        tf = tk.Frame(self.content, bg=C["bg"], padx=20)
        tf.pack(fill="x")
        done_count = len([j for j in jobs if j["status"] == "done"])
        for i, (l, v, cmd) in enumerate([(self.t("active_jobs"), str(active), self.pg_jobs), (self.t("appointments"), str(appts), self.pg_cal), (self.t("outstanding"), f"RM {owed:.0f}", self.pg_invs), (self.t("jobs_done"), str(done_count), self.pg_jobs)]):
            c = tk.Frame(tf, bg=C["card"], bd=1, relief="solid", cursor="hand2")
            c.grid(row=0, column=i, padx=6, pady=6, sticky="nsew")
            c.bind("<Button-1>", lambda e, c=cmd: c())
            tk.Label(c, text=l, bg=C["card"], fg=C["txt2"], font=("Segoe UI", 11), anchor="w", padx=15, pady=8).pack(fill="x")
            tk.Label(c, text=v, bg=C["card"], fg=C["txt"], font=("Segoe UI", 22, "bold"), anchor="w", padx=15, pady=8).pack(fill="x")
            if l == self.t("outstanding") and owed > 0:
                tk.Label(c, text=f"{len(unpaid)} {self.t('unpaid_invoices')}", bg=C["card"], fg=C["err"], font=("Segoe UI", 9), anchor="w", padx=15, pady=6).pack(fill="x")
            c.bind("<Enter>", lambda e, c=c: c.configure(bg=C["card_h"]))
            c.bind("<Leave>", lambda e, c=c: c.configure(bg=C["card"]))
        for i in range(4):
            tf.columnconfigure(i, weight=1)
        rf = tk.Frame(self.content, bg=C["bg"], padx=20, pady=15)
        rf.pack(fill="x")
        rems = []
        for j in jobs:
            if j["status"] == "in-progress" and j["due_date"] and j["due_date"] <= today:
                rems.append(f"{j['job_code']}: {j['item']} - Ready")
        for a in self.db.get_appointments(today):
            rems.append(f"{a['time']} - {a['customer_name'] or 'Walk-in'}")
        if rems:
            tk.Label(rf, text=self.t("reminders"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=8)
            for r in rems[:5]:
                row = tk.Frame(rf, bg="#FEF3C7", bd=1, relief="solid", pady=8, padx=14)
                row.pack(fill="x", pady=3)
                tk.Label(row, text=r, bg="#FEF3C7", fg="#92400E", font=("Segoe UI", 11), anchor="w").pack(fill="x")
        qf = tk.Frame(self.content, bg=C["bg"], padx=20, pady=10)
        qf.pack(fill="x")
        tk.Label(qf, text=self.t("quick_actions"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=8)
        bf = tk.Frame(qf, bg=C["bg"]); bf.pack(fill="x")
        for t, c in [(self.t("new_job"), self.pg_new_job), (self.t("new_customer"), self.pg_new_cust), (self.t("new_appointment"), self.pg_new_appt)]:
            b = self.btn(bf, t, c); b.pack(side="left", padx=4)

        uncollected = self.db.get_uncollected_jobs()
        if uncollected:
            uf = tk.Frame(self.content, bg=C["bg"], padx=20, pady=10)
            uf.pack(fill="x")
            tk.Label(uf, text=f"Waiting for Pickup ({len(uncollected)})", bg=C["bg"], fg=C["warn"], font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=8)
            for j in uncollected[:5]:
                row = tk.Frame(uf, bg="#FEF3C7", bd=1, relief="solid", pady=8, padx=14)
                row.pack(fill="x", pady=3)
                left = tk.Frame(row, bg="#FEF3C7")
                left.pack(side="left", fill="x", expand=True)
                tk.Label(left, text=f"{j['customer_name'] or 'Unknown'} - {j['item']}", bg="#FEF3C7", fg="#92400E", font=("Segoe UI", 11), anchor="w").pack(fill="x")
                tk.Label(left, text=f"Waiting {j['days_waiting']} day(s)", bg="#FEF3C7", fg="#92400E", font=("Segoe UI", 10)).pack(fill="x")
                def send_pickup_reminder(job=j):
                    phone = (job["customer_phone"] or "").replace("+","").replace("-","").replace(" ","")
                    if not phone.startswith("60"):
                        phone = "60" + phone
                    if not phone:
                        return messagebox.showwarning("No Phone", "No phone number for this customer.")
                    biz_name = self.db.get_setting("business_name", "Shop")
                    msg = f"Hi {job['customer_name'] or 'Customer'},\n\n"
                    msg += f"Your {job['item']} service is ready for collection!\n\n"
                    msg += f"Please pick up at your convenience.\n\n"
                    google_review = self.db.get_setting("google_review", "")
                    if google_review:
                        review_link = google_review.rstrip("/") + "/write-review"
                        msg += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
                    msg += f"Thank you!\n{biz_name}"
                    url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                    try:
                        webbrowser.open(url)
                    except:
                        pass
                    messagebox.showinfo("Reminder Sent", f"WhatsApp opened for +{phone}")
                tk.Button(row, text="Send Reminder", command=send_pickup_reminder, bg=C["warn"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=2, cursor="hand2").pack(side="right")

    def pg_jobs(self):
        self.clr()
        self.hdr(self.t("jobs"), self.t("new_job"), self.pg_new_job)
        f = tk.Frame(self.content, bg=C["bg"], padx=20)
        f.pack(fill="both", expand=True)
        sf = tk.Frame(f, bg=C["bg"])
        sf.pack(fill="x", pady=(0,10))
        self.jobs_search_var = tk.StringVar()
        self.jobs_search_var.trace("w", lambda *a: self._filter_jobs())
        tk.Entry(sf, textvariable=self.jobs_search_var, font=("Segoe UI", 11), bd=1, relief="solid").pack(side="left", fill="x", expand=True, ipady=6, padx=(0,10))
        tk.Label(sf, text="Type to filter...", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack(side="left")
        self.jobs_list_frame = tk.Frame(f, bg=C["bg"])
        self.jobs_list_frame.pack(fill="both", expand=True)
        self._filter_jobs()

    def _filter_jobs(self):
        for w in self.jobs_list_frame.winfo_children():
            w.destroy()
        jobs = self.db.get_jobs()
        q = self.jobs_search_var.get().strip().lower()
        if q:
            jobs = [j for j in jobs if q in (j["job_code"]+j["item"]+(j["problem"] or "")+(j["customer_name"] or "")).lower()]
        if not jobs:
            tk.Label(self.jobs_list_frame, text=self.t("no_jobs") if not q else "No results", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
            return
        h = tk.Frame(self.jobs_list_frame, bg=C["bg"]); h.pack(fill="x", pady=8)
        for t, w in [("Code",14),("Item",22),("Customer",16),("Quote",10),("Status",11),("Due",11),("Action",14)]:
            tk.Label(h, text=t, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10, "bold"), width=w, anchor="w").pack(side="left", padx=4)
        sc = {"pending": C["warn"], "in-progress": "#2563EB", "done": C["ok"]}
        for j in jobs:
            r = self.row(self.jobs_list_frame)
            tk.Label(r, text=j["job_code"], bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold"), width=14, anchor="w").pack(side="left", padx=4)
            tk.Label(r, text=j["item"], bg=C["card"], fg=C["txt"], font=("Segoe UI", 10), width=22, anchor="w").pack(side="left", padx=4)
            tk.Label(r, text=j["customer_name"] or "-", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10), width=16, anchor="w").pack(side="left", padx=4)
            tk.Label(r, text=f"RM {j['quote']:.0f}", bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold"), width=10, anchor="w").pack(side="left", padx=4)
            tk.Label(r, text=j["status"].upper(), bg=sc.get(j["status"],"#999"), fg=C["white"], font=("Segoe UI", 9, "bold"), padx=8, pady=2).pack(side="left", padx=4)
            tk.Label(r, text=self.fmt_date(j["due_date"]), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10), width=11, anchor="w").pack(side="left", padx=4)
            tk.Button(r, text="Edit", command=lambda j=j: self.edit_job(j), bg=C["card"], fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=6, cursor="hand2").pack(side="right", padx=2)
            if j["status"] != "done":
                b = tk.Button(r, text="Done", command=lambda j=j: self.mark_done(j), bg=C["ok"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=2, cursor="hand2")
                b.pack(side="right", padx=4)
            if j["status"] == "done":
                invs = self.db.get_invoices()
                has_inv = any(i["job_id"] == j["id"] for i in invs)
                if not has_inv:
                    tk.Button(r, text="PDF", command=lambda j=j: self.download_job_pdf(j), bg="#2563EB", fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, pady=2, cursor="hand2").pack(side="right", padx=2)

    def download_job_pdf(self, job):
        invs = self.db.get_invoices()
        inv = None
        for i in invs:
            if i["job_id"] == job["id"]:
                inv = i
                break
        if not inv:
            inv_id = self.db.add_invoice(job["id"], job["quote"])
            invs = self.db.get_invoices()
            inv = invs[-1]
        cust = self.db.get_customer(job["customer_id"]) if job["customer_id"] else None
        pdf_path = self.generate_invoice_pdf(inv["invoice_code"], job, cust)
        messagebox.showinfo("PDF Saved", f"Invoice PDF saved to:\n{pdf_path}")
        try:
            os.startfile(os.path.dirname(pdf_path))
        except:
            pass

    def pg_new_job(self):
        self.clr()
        self.hdr(self.t("new_job_title"))
        f = tk.Frame(self.content, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        self.je = {}
        cf = tk.Frame(f, bg=C["bg"])
        cf.pack(fill="x", pady=8)
        tk.Label(cf, text=self.t("customer"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        customers = self.db.get_customers()
        cust_names = [c["name"] for c in customers] if customers else []
        self.cust_map = {c["name"]: c for c in customers} if customers else {}
        self.je["Customer"] = tk.StringVar()
        self.cust_entry = tk.Entry(cf, font=("Segoe UI", 12), bd=1, relief="solid")
        self.cust_entry.pack(side="left", fill="x", expand=True, ipady=6)
        if cust_names:
            tk.Label(cf, text="Or pick:", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack(side="left", padx=(10,5))
            self.cust_menu_var = tk.StringVar()
            menu = tk.OptionMenu(cf, self.cust_menu_var, *cust_names, command=self._pick_cust)
            menu.configure(font=("Segoe UI", 10), width=15)
            menu.pack(side="left", ipady=4)
        pf = tk.Frame(f, bg=C["bg"])
        pf.pack(fill="x", pady=8)
        tk.Label(pf, text=self.t("phone"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        self.je["Phone"] = tk.Entry(pf, font=("Segoe UI", 12), bd=1, relief="solid")
        self.je["Phone"].insert(0, "+60")
        self.je["Phone"].pack(side="left", fill="x", expand=True, ipady=6)
        ef = tk.Frame(f, bg=C["bg"])
        ef.pack(fill="x", pady=8)
        tk.Label(ef, text="Email", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        self.je["Email"] = tk.Entry(ef, font=("Segoe UI", 12), bd=1, relief="solid")
        self.je["Email"].pack(side="left", fill="x", expand=True, ipady=6)
        for l in ["Item", "Problem", "Quote (RM)", "Notes"]:
            self.je[l] = self.field(f, self.t(l.lower()))
        self.je["Due Date"] = self.date_field(f, self.t("due_date"))
        bf = tk.Frame(f, bg=C["bg"], pady=20); bf.pack(fill="x")
        self.btn(bf, self.t("save"), self.save_job).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=self.pg_jobs, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def _pick_cust(self, name):
        if name in self.cust_map:
            c = self.cust_map[name]
            self.cust_entry.delete(0, tk.END)
            self.cust_entry.insert(0, c["name"])
            self.je["Phone"].delete(0, tk.END)
            self.je["Phone"].insert(0, c["phone"] or "+60")
            self.je["Email"].delete(0, tk.END)
            self.je["Email"].insert(0, c["email"] or "")

    def save_job(self):
        cust_name = self.cust_entry.get().strip()
        phone = self.je["Phone"].get().strip()
        email = self.je["Email"].get().strip()
        item = self.je["Item"].get().strip()
        if not item:
            return messagebox.showerror("Error", "Enter item")
        try:
            q = float(self.je["Quote (RM)"].get().strip() or "0")
        except:
            return messagebox.showerror("Error", "Quote must be number")
        if self.is_demo() and len(self.db.get_jobs()) >= 10:
            return messagebox.showerror("Demo Limit", "Demo mode is limited to 10 jobs.\nPlease activate with a license key.")
        cid = None
        if cust_name:
            if cust_name in self.cust_map:
                cid = self.cust_map[cust_name]["id"]
            else:
                cid = self.db.add_customer(cust_name, phone, email)
        due = self.je["Due Date"].get() if isinstance(self.je["Due Date"], tk.StringVar) else self.je["Due Date"].get().strip()
        self.db.add_job(cid, item, self.je["Problem"].get().strip(), q, due, self.je["Notes"].get().strip())
        messagebox.showinfo("Done", "Job saved")
        self.pg_jobs()

    def edit_job(self, j):
        win = tk.Toplevel(self.root)
        win.title("Edit Job")
        win.geometry("500x550")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text="Edit Job", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 16, "bold")).pack(pady=10)
        f = tk.Frame(win, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        item_e = self.field(f, self.t("item"), j["item"])
        problem_e = self.field(f, self.t("problem"), j["problem"] or "")
        quote_e = self.field(f, self.t("quote"), str(j["quote"]))
        status_frame = tk.Frame(f, bg=C["bg"])
        status_frame.pack(fill="x", pady=8)
        tk.Label(status_frame, text="Status", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        status_var = tk.StringVar(value=j["status"])
        for v, lbl in [("pending","Pending"),("in-progress","In-Progress"),("done","Done")]:
            tk.Radiobutton(status_frame, text=lbl, variable=status_var, value=v, bg=C["bg"], font=("Segoe UI", 11)).pack(side="left", padx=5)
        due_var = self.date_field(f, self.t("due_date"), j["due_date"])
        notes_e = self.field(f, self.t("notes"), j["notes"] or "")
        bf = tk.Frame(f, bg=C["bg"], pady=15)
        bf.pack(fill="x")
        def save():
            try:
                q = float(quote_e.get().strip() or "0")
            except:
                return messagebox.showerror("Error", "Quote must be number")
            due = due_var.get() if isinstance(due_var, tk.StringVar) else due_var.get().strip()
            self.db.update_job(j["id"], item_e.get().strip(), problem_e.get().strip(), q, status_var.get(), due, notes_e.get().strip())
            win.destroy()
            messagebox.showinfo("Done", "Job updated")
            self._filter_jobs()
        self.btn(bf, self.t("save"), save, bg=C["ok"]).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=win.destroy, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def _job_has_invoice(self, job_id):
        for i in self.db.get_invoices():
            if i["job_id"] == job_id:
                return True
        return False

    def _get_or_create_invoice(self, job):
        invs = self.db.get_invoices()
        for i in invs:
            if i["job_id"] == job["id"]:
                return i
        self.db.add_invoice(job["id"], job["quote"])
        invs = self.db.get_invoices()
        return invs[-1] if invs else None

    def mark_done(self, job):
        self.db.update_job_status(job["id"], "done")
        win = tk.Toplevel(self.root)
        win.title("Job Complete")
        win.geometry("360x400")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text="Job Complete!", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 16, "bold")).pack(pady=8)
        tk.Label(win, text=job["item"], bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 12)).pack()
        tk.Label(win, text=f"RM {job['quote']:.2f}", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 14, "bold")).pack(pady=5)
        cust = self.db.get_customer(job["customer_id"]) if job["customer_id"] else None
        has_inv = self._job_has_invoice(job["id"])
        if has_inv:
            tk.Label(win, text="(Invoice already exists)", bg=C["bg"], fg=C["warn"], font=("Segoe UI", 9)).pack()
        def send_inv():
            inv = self._get_or_create_invoice(job)
            inv_code = inv["invoice_code"] if inv else "N/A"
            phone = ""
            if cust and cust["phone"]:
                phone = cust["phone"].replace("+","").replace("-","").replace(" ","")
                if not phone.startswith("60"):
                    phone = "60" + phone
            win.destroy()
            use_pdf = self.db.get_setting("invoice_format", "text") == "pdf"
            pdf_path = None
            if use_pdf:
                pdf_path = self.generate_invoice_pdf(inv_code, job, cust)
            if phone:
                msg = f"Hi {cust['name'] if cust else 'Customer'},\n\n"
                msg += f"Your {job['item']} service is ready for collection!\n\n"
                if job['problem']:
                    msg += f"Service: {job['problem']}\n"
                msg += f"Ready since: {self.fmt_date(datetime.now().strftime('%Y-%m-%d'))}\n\n"
                msg += f"Please pick up at your convenience.\n\n"
                msg += f"Invoice: {inv_code}\n"
                msg += f"Amount: RM {job['quote']:.2f}\n\n"
                google_review = self.db.get_setting("google_review", "")
                if google_review:
                    review_link = google_review.rstrip("/") + "/write-review"
                    msg += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
                msg += f"Thank you for your business!\n{self.db.get_setting('business_name', 'Shop')}"
                url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                try:
                    webbrowser.open(url)
                except:
                    pass
                if use_pdf:
                    messagebox.showinfo("Done", f"Invoice created! WhatsApp opened for +{phone}\nPDF saved to: {pdf_path}")
                else:
                    messagebox.showinfo("Done", f"Invoice created! WhatsApp opened for +{phone}")
            else:
                messagebox.showwarning("Warning", "Invoice created but no phone number. Add phone to customer first.")
            self.pg_jobs()
        def send_email_inv():
            inv = self._get_or_create_invoice(job)
            inv_code = inv["invoice_code"] if inv else "N/A"
            email = ""
            if cust and cust["email"]:
                email = cust["email"]
            win.destroy()
            use_pdf = self.db.get_setting("invoice_format", "text") == "pdf"
            if email:
                biz_name = self.db.get_setting('business_name', 'Shop')
                subject = f"Invoice {inv_code} from {biz_name}"
                if use_pdf:
                    pdf_path = self.generate_invoice_pdf(inv_code, job, cust)
                    body = f"Dear {cust['name'] if cust else 'Customer'},\n\n"
                    body += f"Please find attached invoice {inv_code}.\n\n"
                    body += f"Amount: RM {job['quote']:.2f}\n\n"
                    google_review = self.db.get_setting("google_review", "")
                    if google_review:
                        review_link = google_review.rstrip("/") + "/write-review"
                        body += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
                    body += f"Thank you!\n{biz_name}"
                    mailto = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
                    try:
                        webbrowser.open(mailto)
                        os.startfile(pdf_path)
                    except:
                        pass
                    messagebox.showinfo("Done", f"Invoice created! Email opened for {email}\nPDF saved to: {pdf_path}")
                else:
                    body = f"Dear {cust['name'] if cust else 'Customer'},\n\n"
                    body += f"Thank you for your business!\n\n"
                    body += f"Invoice: {inv_code}\nDate: {self.fmt_date(datetime.now().strftime('%Y-%m-%d'))}\nItem: {job['item']}\nService: {job['problem'] or 'N/A'}\nAmount: RM {job['quote']:.2f}\n\n"
                    google_review = self.db.get_setting("google_review", "")
                    if google_review:
                        review_link = google_review.rstrip("/") + "/write-review"
                        body += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
                    body += f"Thank you!\n{biz_name}"
                    mailto = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
                    try:
                        webbrowser.open(mailto)
                    except:
                        pass
                    messagebox.showinfo("Done", f"Invoice created! Email opened for {email}")
            else:
                messagebox.showwarning("Warning", "Invoice created but no email. Add email to customer first.")
            self.pg_jobs()
        def just_inv():
            self._get_or_create_invoice(job)
            win.destroy()
            messagebox.showinfo("Done", "Invoice created")
            self.pg_jobs()
        self.btn(win, "Invoice + WhatsApp", send_inv).pack(fill="x", padx=25, pady=5)
        self.btn(win, "Invoice + Email", send_email_inv, bg="#2563EB").pack(fill="x", padx=25, pady=5)
        self.btn(win, "Just Invoice", just_inv, bg=C["card"], fg=C["txt"]).pack(fill="x", padx=25, pady=5)
        tk.Button(win, text="Skip", command=win.destroy, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10), bd=0, cursor="hand2").pack(pady=10)

    def pg_custs(self):
        self.clr()
        self.hdr(self.t("customers"), self.t("new_customer"), self.pg_new_cust)
        f = tk.Frame(self.content, bg=C["bg"], padx=20)
        f.pack(fill="both", expand=True)
        sf = tk.Frame(f, bg=C["bg"])
        sf.pack(fill="x", pady=(0,10))
        self.cust_search_var = tk.StringVar()
        self.cust_search_var.trace("w", lambda *a: self._filter_custs())
        tk.Entry(sf, textvariable=self.cust_search_var, font=("Segoe UI", 11), bd=1, relief="solid").pack(side="left", fill="x", expand=True, ipady=6, padx=(0,10))
        tk.Label(sf, text="Type to filter...", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack(side="left")
        self.cust_list_frame = tk.Frame(f, bg=C["bg"])
        self.cust_list_frame.pack(fill="both", expand=True)
        self._filter_custs()

    def _filter_custs(self):
        for w in self.cust_list_frame.winfo_children():
            w.destroy()
        cs = self.db.get_customers()
        q = self.cust_search_var.get().strip().lower()
        if q:
            cs = [c for c in cs if q in (c["name"]+(c["phone"] or "")+(c["email"] or "")).lower()]
        if not cs:
            tk.Label(self.cust_list_frame, text=self.t("no_customers") if not q else "No results", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
            return
        for c in cs:
            r = self.row(self.cust_list_frame)
            tk.Label(r, text=c["name"], bg=C["card"], fg=C["txt"], font=("Segoe UI", 12, "bold"), anchor="w").pack(side="left")
            tk.Label(r, text=c["phone"] or "", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 11), anchor="w", padx=20).pack(side="left")
            if c["email"]:
                tk.Label(r, text=c["email"], bg=C["card"], fg=C["txt3"], font=("Segoe UI", 10), anchor="w", padx=15).pack(side="left")
            tk.Button(r, text="Edit", command=lambda c=c: self.edit_cust(c), bg=C["card"], fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=8, cursor="hand2").pack(side="right")

    def edit_cust(self, c):
        win = tk.Toplevel(self.root)
        win.title("Edit Customer")
        win.geometry("450x350")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text="Edit Customer", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 16, "bold")).pack(pady=10)
        f = tk.Frame(win, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        name_e = self.field(f, self.t("name"), c["name"])
        phone_e = self.field(f, self.t("phone"), c["phone"] or "+60")
        email_e = self.field(f, self.t("email"), c["email"] or "")
        notes_e = self.field(f, self.t("notes"), c["notes"] or "")
        bf = tk.Frame(f, bg=C["bg"], pady=15)
        bf.pack(fill="x")
        def save():
            n = name_e.get().strip()
            if not n:
                return messagebox.showerror("Error", "Enter name")
            self.db.update_customer(c["id"], n, phone_e.get().strip(), email_e.get().strip(), c["address"], notes_e.get().strip())
            win.destroy()
            messagebox.showinfo("Done", "Customer updated")
            self._filter_custs()
        self.btn(bf, self.t("save"), save, bg=C["ok"]).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=win.destroy, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def pg_new_cust(self):
        self.clr()
        self.hdr(self.t("new_customer_title"))
        f = tk.Frame(self.content, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        self.ce = {}
        for l, d in [("Name",""), ("Phone","+60"), ("Email",""), ("Notes","")]:
            self.ce[l] = self.field(f, self.t(l.lower()) if l.lower() in ["name","phone","notes"] else l, d)
        bf = tk.Frame(f, bg=C["bg"], pady=20); bf.pack(fill="x")
        self.btn(bf, self.t("save"), self.save_cust).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=self.pg_custs, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def save_cust(self):
        n = self.ce["Name"].get().strip()
        if not n:
            return messagebox.showerror("Error", "Enter name")
        self.db.add_customer(n, self.ce["Phone"].get().strip(), self.ce["Email"].get().strip(), None, self.ce["Notes"].get().strip())
        messagebox.showinfo("Done", "Customer saved")
        self.pg_custs()

    def pg_cal(self):
        self.clr()
        self.hdr(self.t("appointments"), self.t("new_appointment"), self.pg_new_appt)
        f = tk.Frame(self.content, bg=C["bg"], padx=20)
        f.pack(fill="both", expand=True)
        sf = tk.Frame(f, bg=C["bg"])
        sf.pack(fill="x", pady=(0,10))
        self.appt_search_var = tk.StringVar()
        self.appt_search_var.trace("w", lambda *a: self._filter_appts())
        tk.Entry(sf, textvariable=self.appt_search_var, font=("Segoe UI", 11), bd=1, relief="solid").pack(side="left", fill="x", expand=True, ipady=6, padx=(0,10))
        tk.Label(sf, text="Type to filter...", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack(side="left")
        self.appt_list_frame = tk.Frame(f, bg=C["bg"])
        self.appt_list_frame.pack(fill="both", expand=True)
        self._filter_appts()

    def _filter_appts(self):
        for w in self.appt_list_frame.winfo_children():
            w.destroy()
        q = self.appt_search_var.get().strip()
        if q:
            appts = self.db.search_appointments(q)
            if not appts:
                tk.Label(self.appt_list_frame, text="No results", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
                return
            for a in appts:
                r = self.row(self.appt_list_frame)
                tk.Label(r, text=a["date"], bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10), width=12, anchor="w").pack(side="left", padx=4)
                tk.Label(r, text=a["time"], bg=C["card"], fg=C["txt"], font=("Segoe UI", 14, "bold"), width=8, anchor="w").pack(side="left", padx=4)
                tk.Label(r, text=a["customer_name"] or "Walk-in", bg=C["card"], fg=C["txt"], font=("Segoe UI", 12, "bold"), anchor="w").pack(side="left", padx=15)
                tk.Label(r, text=a["purpose"] or "", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 11), anchor="w", padx=15).pack(side="left")
                tk.Button(r, text="Edit", command=lambda a=a: self.edit_appt(a), bg=C["card"], fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=6, cursor="hand2").pack(side="right")
        else:
            today = datetime.now().strftime("%Y-%m-%d")
            tk.Label(self.appt_list_frame, text=self.fmt_date(today), bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 12)).pack(anchor="w", pady=8)
            appts = self.db.get_appointments(today)
            if not appts:
                tk.Label(self.appt_list_frame, text=self.t("no_appointments"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
                return
            for a in appts:
                r = self.row(self.appt_list_frame)
                tk.Label(r, text=a["time"], bg=C["card"], fg=C["txt"], font=("Segoe UI", 14, "bold"), width=8, anchor="w").pack(side="left")
                tk.Label(r, text=a["customer_name"] or "Walk-in", bg=C["card"], fg=C["txt"], font=("Segoe UI", 12, "bold"), anchor="w").pack(side="left", padx=15)
                tk.Label(r, text=a["purpose"] or "", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 11), anchor="w", padx=15).pack(side="left")
                tk.Button(r, text="Edit", command=lambda a=a: self.edit_appt(a), bg=C["card"], fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=6, cursor="hand2").pack(side="right")

    def edit_appt(self, a):
        win = tk.Toplevel(self.root)
        win.title("Edit Appointment")
        win.geometry("500x450")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text="Edit Appointment", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 16, "bold")).pack(pady=10)
        f = tk.Frame(win, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        cust_name_e = self.field(f, self.t("customer"), a["customer_name"] or "")
        date_var = tk.StringVar(value=a["date"])
        date_frame = tk.Frame(f, bg=C["bg"])
        date_frame.pack(fill="x", pady=8)
        tk.Label(date_frame, text=self.t("date"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        date_entry = tk.Entry(date_frame, textvariable=date_var, font=("Segoe UI", 12), bd=1, relief="solid", width=12)
        date_entry.pack(side="left")
        time_parts = a["time"].split(":") if a["time"] else ["09", "00"]
        hour_var = tk.StringVar(value=time_parts[0])
        min_var = tk.StringVar(value=time_parts[1] if len(time_parts) > 1 else "00")
        time_frame = tk.Frame(f, bg=C["bg"])
        time_frame.pack(fill="x", pady=8)
        tk.Label(time_frame, text=self.t("time"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=18, anchor="w").pack(side="left")
        hours = [str(i).zfill(2) for i in range(24)]
        h_menu = tk.OptionMenu(time_frame, hour_var, *hours)
        h_menu.configure(font=("Segoe UI", 11), width=3, bg=C["white"])
        h_menu.pack(side="left")
        tk.Label(time_frame, text=":", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 14, "bold")).pack(side="left", padx=4)
        mins = ["00", "15", "30", "45"]
        m_menu = tk.OptionMenu(time_frame, min_var, *mins)
        m_menu.configure(font=("Segoe UI", 11), width=3, bg=C["white"])
        m_menu.pack(side="left")
        purpose_e = self.field(f, self.t("purpose"), a["purpose"] or "")
        notes_e = self.field(f, self.t("notes"), a["notes"] or "")
        bf = tk.Frame(f, bg=C["bg"], pady=15)
        bf.pack(fill="x")
        def save():
            d = date_var.get().strip()
            if not d:
                return messagebox.showerror("Error", "Enter date")
            t = f"{hour_var.get()}:{min_var.get()}"
            self.db.update_appointment(a["id"], d, t, purpose_e.get().strip(), a["status"], notes_e.get().strip())
            win.destroy()
            messagebox.showinfo("Done", "Appointment updated")
            self.pg_cal()
        self.btn(bf, self.t("save"), save, bg=C["ok"]).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=win.destroy, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def pg_new_appt(self):
        self.clr()
        self.hdr(self.t("new_appointment_title"))
        f = tk.Frame(self.content, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        self.ae = {}
        self.ae["Customer"] = self.field(f, self.t("customer"))
        self.ae["Date"] = self.date_field(f, self.t("date"))
        self.ae["Time"] = self.time_field(f, self.t("time"))
        self.ae["Purpose"] = self.field(f, self.t("purpose"))
        self.ae["Notes"] = self.field(f, self.t("notes"))
        bf = tk.Frame(f, bg=C["bg"], pady=20); bf.pack(fill="x")
        self.btn(bf, self.t("save"), self.save_appt).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=self.pg_cal, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def save_appt(self):
        c = self.ae["Customer"].get().strip()
        d = self.ae["Date"].get() if isinstance(self.ae["Date"], tk.StringVar) else self.ae["Date"].get().strip()
        h = self.ae["Time"][0].get()
        m = self.ae["Time"][1].get()
        t = f"{h}:{m}"
        if not d:
            return messagebox.showerror("Error", "Enter date")
        cid = None
        if c:
            cs = self.db.get_customers(c)
            cid = cs[0]["id"] if cs else self.db.add_customer(c)
        self.db.add_appointment(cid, d, t, self.ae["Purpose"].get().strip(), self.ae["Notes"].get().strip())
        messagebox.showinfo("Done", "Appointment saved")
        self.pg_cal()

    def pg_invs(self):
        self.clr()
        self.hdr(self.t("invoices"), self.t("from_job"), self.pg_new_inv)
        f = tk.Frame(self.content, bg=C["bg"], padx=20)
        f.pack(fill="both", expand=True)
        sf = tk.Frame(f, bg=C["bg"])
        sf.pack(fill="x", pady=(0,10))
        self.inv_search_var = tk.StringVar()
        self.inv_search_var.trace("w", lambda *a: self._filter_invs())
        tk.Entry(sf, textvariable=self.inv_search_var, font=("Segoe UI", 11), bd=1, relief="solid").pack(side="left", fill="x", expand=True, ipady=6, padx=(0,10))
        tk.Label(sf, text="Type to filter...", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack(side="left")
        self.inv_list_frame = tk.Frame(f, bg=C["bg"])
        self.inv_list_frame.pack(fill="both", expand=True)
        self._filter_invs()

    def _filter_invs(self):
        for w in self.inv_list_frame.winfo_children():
            w.destroy()
        invs = self.db.get_invoices()
        q = self.inv_search_var.get().strip().lower()
        if q:
            invs = [i for i in invs if q in (i["invoice_code"]+(i["customer_name"] or "")).lower()]
        if not invs:
            tk.Label(self.inv_list_frame, text=self.t("no_invoices") if not q else "No results", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
            return
        unpaid = [i for i in invs if not i["paid"]]
        paid = [i for i in invs if i["paid"]]
        if unpaid:
            total_owed = sum(i["amount"] for i in unpaid)
            hdr = tk.Frame(self.inv_list_frame, bg=C["bg"])
            hdr.pack(fill="x", pady=5)
            tk.Label(hdr, text=f"{self.t('unpaid')} ({len(unpaid)} invoices, RM {total_owed:.2f} total)", bg=C["bg"], fg=C["err"], font=("Segoe UI", 13, "bold")).pack(side="left")
            for i in unpaid:
                r = self.row(self.inv_list_frame)
                r.configure(bg="#FEF2F2")
                left = tk.Frame(r, bg="#FEF2F2")
                left.pack(side="left", fill="x", expand=True)
                tk.Label(left, text=i["invoice_code"], bg="#FEF2F2", fg=C["txt"], font=("Segoe UI", 11, "bold"), anchor="w").pack(side="left")
                tk.Label(left, text=i["customer_name"] or "Unknown", bg="#FEF2F2", fg=C["txt"], font=("Segoe UI", 11), anchor="w", padx=15).pack(side="left")
                tk.Label(left, text=f"RM {i['amount']:.2f}", bg="#FEF2F2", fg=C["err"], font=("Segoe UI", 12, "bold"), anchor="w", padx=15).pack(side="left")
                right = tk.Frame(r, bg="#FEF2F2")
                right.pack(side="right")
                tk.Button(right, text="Email", command=lambda inv=i: self.send_email(inv), bg="#2563EB", fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=2, cursor="hand2").pack(side="left", padx=3)
                tk.Button(right, text=self.t("send_whatsapp"), command=lambda inv=i: self.send_whatsapp(inv), bg=C["ok"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=2, cursor="hand2").pack(side="left", padx=3)
                tk.Button(right, text="PDF", command=lambda inv=i: self.download_inv_pdf(inv), bg="#7C3AED", fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=2, cursor="hand2").pack(side="left", padx=3)
                tk.Button(right, text=self.t("mark_paid"), command=lambda iid=i["id"]: self.mark_paid(iid), bg=C["warn"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=2, cursor="hand2").pack(side="left")
        if paid:
            tk.Label(self.inv_list_frame, text=f"{self.t('paid')} ({len(paid)})", bg=C["bg"], fg=C["ok"], font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=10)
            for i in paid:
                r = self.row(self.inv_list_frame)
                tk.Label(r, text=i["invoice_code"], bg=C["card"], fg=C["txt"], font=("Segoe UI", 11, "bold"), anchor="w").pack(side="left")
                tk.Label(r, text=i["customer_name"] or "Unknown", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 11), anchor="w", padx=15).pack(side="left")
                tk.Label(r, text=f"RM {i['amount']:.2f}", bg=C["card"], fg=C["txt"], font=("Segoe UI", 11, "bold"), anchor="w", padx=15).pack(side="left")
                method = i["payment_method"] or ""
                if method:
                    method_bg = {"Cash": C["ok"], "E-Wallet": "#2563EB", "Card": "#7C3AED", "Transfer": C["warn"]}.get(method, C["txt3"])
                    tk.Label(r, text=method, bg=method_bg, fg=C["white"], font=("Segoe UI", 9, "bold"), padx=8, pady=2).pack(side="right", padx=5)
                tk.Label(r, text="PAID", bg=C["ok"], fg=C["white"], font=("Segoe UI", 9, "bold"), padx=10, pady=2).pack(side="right")

    def download_inv_pdf(self, inv):
        job = None
        for j in self.db.get_jobs():
            if j["id"] == inv["job_id"]:
                job = j
                break
        cust = None
        if job and job["customer_id"]:
            cust = self.db.get_customer(job["customer_id"])
        pdf_path = self.generate_invoice_pdf(inv["invoice_code"], job, cust)
        messagebox.showinfo("PDF Saved", f"Invoice PDF saved to:\n{pdf_path}")
        try:
            os.startfile(os.path.dirname(pdf_path))
        except:
            pass

    def send_whatsapp(self, inv):
        job = self.db.get_jobs()
        job_for_inv = None
        for j in job:
            if j["id"] == inv["job_id"]:
                job_for_inv = j
                break
        cust = None
        if job_for_inv and job_for_inv["customer_id"]:
            cust = self.db.get_customer(job_for_inv["customer_id"])
        phone = ""
        if cust and cust["phone"]:
            phone = cust["phone"].replace("+","").replace("-","").replace(" ","")
            if not phone.startswith("60"):
                phone = "60" + phone
        if not phone:
            return messagebox.showwarning("No Phone", "No phone number found for this customer.")
        use_pdf = self.db.get_setting("invoice_format", "text") == "pdf"
        if use_pdf:
            pdf_path = self.generate_invoice_pdf(inv["invoice_code"], job_for_inv, cust)
        msg = f"Hi {cust['name'] if cust else 'Customer'},\n\n"
        msg += f"This is a friendly reminder for your unpaid invoice.\n\n"
        msg += f"Invoice: {inv['invoice_code']}\n"
        if job_for_inv:
            msg += f"Item: {job_for_inv['item']}\n"
            if job_for_inv['problem']:
                msg += f"Service: {job_for_inv['problem']}\n"
        msg += f"Amount: RM {inv['amount']:.2f}\n\n"
        msg += f"Please make payment at your convenience.\n\n"
        google_review = self.db.get_setting("google_review", "")
        if google_review:
            review_link = google_review.rstrip("/") + "/write-review"
            msg += f"\nWe'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
        msg += f"Thank you!\n{self.db.get_setting('business_name', 'Shop')}"
        url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
        try:
            webbrowser.open(url)
        except:
            pass
        if use_pdf:
            messagebox.showinfo("WhatsApp", f"Opening WhatsApp for +{phone}\nPDF saved to: {pdf_path}")
        else:
            messagebox.showinfo("WhatsApp", f"Opening WhatsApp for +{phone}")

    def send_email(self, inv):
        job = self.db.get_jobs()
        job_for_inv = None
        for j in job:
            if j["id"] == inv["job_id"]:
                job_for_inv = j
                break
        cust = None
        if job_for_inv and job_for_inv["customer_id"]:
            cust = self.db.get_customer(job_for_inv["customer_id"])
        email = ""
        if cust and cust["email"]:
            email = cust["email"]
        if not email:
            return messagebox.showwarning("No Email", "No email found for this customer.\nAdd email to customer first.")
        biz_name = self.db.get_setting('business_name', 'Shop')
        subject = f"Invoice {inv['invoice_code']} from {biz_name}"
        use_pdf = self.db.get_setting("invoice_format", "text") == "pdf"
        if use_pdf:
            pdf_path = self.generate_invoice_pdf(inv["invoice_code"], job_for_inv, cust)
            body = f"Dear {cust['name'] if cust else 'Customer'},\n\n"
            body += f"Please find attached invoice {inv['invoice_code']}.\n\n"
            body += f"Amount: RM {inv['amount']:.2f}\n\n"
            google_review = self.db.get_setting("google_review", "")
            if google_review:
                review_link = google_review.rstrip("/") + "/write-review"
                body += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
            body += f"Thank you!\n{biz_name}"
            mailto = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            try:
                webbrowser.open(mailto)
                os.startfile(pdf_path)
            except:
                pass
            messagebox.showinfo("Email", f"Email opened for {email}\nPDF saved to: {pdf_path}")
        else:
            body = f"Dear {cust['name'] if cust else 'Customer'},\n\n"
            body += f"Thank you for your business!\n\n"
            body += f"Invoice: {inv['invoice_code']}\n"
            body += f"Date: {self.fmt_date(datetime.now().strftime('%Y-%m-%d'))}\n"
            if job_for_inv:
                body += f"Item: {job_for_inv['item']}\n"
                body += f"Service: {job_for_inv['problem'] or 'N/A'}\n"
            body += f"Amount: RM {inv['amount']:.2f}\n"
            body += f"Status: UNPAID\n\n"
            body += f"Please make payment at your earliest convenience.\n\n"
            google_review = self.db.get_setting("google_review", "")
            if google_review:
                review_link = google_review.rstrip("/") + "/write-review"
                body += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
            body += f"Thank you!\n{biz_name}"
            mailto = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            try:
                webbrowser.open(mailto)
            except:
                pass
            messagebox.showinfo("Email", f"Opening email client for {email}")

    def generate_invoice_pdf(self, inv_code, job, cust):
        invoice_dir = os.path.join(APP_DIR, "data", "invoices")
        os.makedirs(invoice_dir, exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 22)
        pdf.cell(0, 12, "INVOICE", new_x="LMARGIN", new_y="NEXT", align="R")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, f"Invoice: {inv_code}", new_x="LMARGIN", new_y="NEXT", align="R")
        pdf.cell(0, 6, f"Date: {self.fmt_date(datetime.now().strftime('%Y-%m-%d'))}", new_x="LMARGIN", new_y="NEXT", align="R")
        pdf.cell(0, 6, f"Status: UNPAID", new_x="LMARGIN", new_y="NEXT", align="R")
        pdf.ln(8)
        biz_name = self.db.get_setting("business_name", "Shop")
        biz_phone = self.db.get_setting("business_phone", "")
        biz_email = self.db.get_setting("business_email", "")
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 8, biz_name, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        if biz_phone:
            pdf.cell(0, 6, f"Phone: {biz_phone}", new_x="LMARGIN", new_y="NEXT")
        if biz_email:
            pdf.cell(0, 6, f"Email: {biz_email}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(8)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 7, "Bill To:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        if cust:
            pdf.cell(0, 6, cust["name"], new_x="LMARGIN", new_y="NEXT")
            if cust["phone"]:
                pdf.cell(0, 6, f"Phone: {cust['phone']}", new_x="LMARGIN", new_y="NEXT")
            if cust["email"]:
                pdf.cell(0, 6, f"Email: {cust['email']}", new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.cell(0, 6, "Walk-in Customer", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(8)
        pdf.set_fill_color(50, 50, 50)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(80, 8, "  Item", fill=True)
        pdf.cell(55, 8, "  Service", fill=True)
        pdf.cell(35, 8, "  Amount", new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)
        item = job["item"] if job else "N/A"
        problem = (job["problem"] or "N/A") if job else "N/A"
        pdf.cell(80, 8, f"  {item}")
        pdf.cell(55, 8, f"  {problem}")
        pdf.cell(35, 8, f"  RM {job['quote']:.2f}" if job else "  RM 0.00", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(135, 10, "Total:")
        pdf.cell(35, 10, f"RM {job['quote']:.2f}" if job else "RM 0.00", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)
        google_review = self.db.get_setting("google_review", "")
        if google_review:
            review_link = google_review.rstrip("/") + "/write-review"
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, "We'd love your feedback!", new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 6, "Leave us a Google review:", new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.set_text_color(0, 102, 204)
            pdf.cell(0, 6, review_link, new_x="LMARGIN", new_y="NEXT", align="C", link=review_link)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, "Thank you for your business!", new_x="LMARGIN", new_y="NEXT", align="C")
        filename = f"{inv_code}.pdf"
        filepath = os.path.join(invoice_dir, filename)
        pdf.output(filepath)
        return filepath

    def mark_paid(self, iid):
        win = tk.Toplevel(self.root)
        win.title("Payment")
        win.geometry("280x220")
        win.configure(bg=C["bg"])
        tk.Label(win, text=self.t("how_paid"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(pady=15)
        for m in ["Cash", "E-Wallet", "Card", "Transfer"]:
            b = self.btn(win, self.t(m.lower().replace("-","_")), lambda m=m: [self.db.mark_invoice_paid(iid, m), win.destroy(), self.pg_invs()])
            b.pack(fill="x", padx=30, pady=3)

    def pg_new_inv(self):
        self.clr()
        self.hdr(self.t("create_invoice"))
        f = tk.Frame(self.content, bg=C["bg"], padx=20)
        f.pack(fill="both", expand=True)
        jobs = self.db.get_jobs(status="done")
        if not jobs:
            tk.Label(f, text=self.t("no_jobs"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
            return
        for j in jobs:
            r = self.row(f)
            tk.Label(r, text=f"{j['job_code']} - {j['item']}", bg=C["card"], fg=C["txt"], font=("Segoe UI", 11, "bold"), anchor="w").pack(side="left")
            tk.Label(r, text=f"RM {j['quote']:.2f}", bg=C["card"], fg=C["txt"], font=("Segoe UI", 11, "bold"), anchor="w", padx=15).pack(side="left")
            tk.Button(r, text="Create", command=lambda j=j: [self.db.add_invoice(j["id"], j["quote"]), messagebox.showinfo("Done", "Invoice created"), self.pg_invs()], bg=C["pri"], fg=C["white"], font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2").pack(side="right")

    def pg_rpt(self):
        self.clr()
        self.hdr(self.t("reports"))
        today = datetime.now().strftime("%Y-%m-%d")
        week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        jobs = self.db.get_jobs()
        invs = self.db.get_invoices()
        paid = [i for i in invs if i["paid"]]
        unpaid = [i for i in invs if not i["paid"]]
        today_rev = sum(i["amount"] for i in paid if i["created_at"][:10] == today)
        week_rev = sum(i["amount"] for i in paid if i["created_at"][:10] >= week)
        month_rev = sum(i["amount"] for i in paid if i["created_at"][:10] >= month)
        outstanding = sum(i["amount"] for i in unpaid)
        total_earned = sum(i["amount"] for i in paid)
        sf = tk.Frame(self.content, bg=C["bg"], padx=20)
        sf.pack(fill="x")
        cards = [
            ("Revenue Today", f"RM {today_rev:.2f}", "Money collected today", C["ok"]),
            ("Revenue This Week", f"RM {week_rev:.2f}", "Money collected this week", C["ok"]),
            ("Revenue This Month", f"RM {month_rev:.2f}", "Money collected this month", C["ok"]),
            ("Outstanding", f"RM {outstanding:.2f}", "Still owed by customers", C["err"] if outstanding > 0 else C["ok"]),
        ]
        for i, (title, value, desc, color) in enumerate(cards):
            c = tk.Frame(sf, bg=C["card"], bd=1, relief="solid", pady=12, padx=18)
            c.grid(row=0, column=i, padx=6, pady=8, sticky="nsew")
            tk.Label(c, text=title, bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w")
            tk.Label(c, text=value, bg=C["card"], fg=color, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=5)
            tk.Label(c, text=desc, bg=C["card"], fg=C["txt3"], font=("Segoe UI", 9)).pack(anchor="w", pady=2)
        for i in range(4):
            sf.columnconfigure(i, weight=1)
        st = tk.Frame(self.content, bg=C["bg"], padx=20, pady=15)
        st.pack(fill="both", expand=True)
        tk.Label(st, text="Summary", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=10)
        summary = [
            ("Total Earned (All Time)", f"RM {total_earned:.2f}", C["ok"]),
            ("Outstanding (Unpaid)", f"RM {outstanding:.2f}", C["err"] if outstanding > 0 else C["ok"]),
            ("Total Jobs", str(len(jobs)), C["txt"]),
            ("Completed Jobs", str(len([j for j in jobs if j["status"]=="done"])), C["ok"]),
            ("Active Jobs", str(len([j for j in jobs if j["status"]!="done"])), C["warn"]),
            ("Total Customers", str(len(self.db.get_customers())), C["txt"]),
            ("Paid Invoices", str(len(paid)), C["ok"]),
            ("Unpaid Invoices", str(len(unpaid)), C["err"] if unpaid else C["ok"]),
        ]
        for label, value, color in summary:
            r = self.row(st)
            tk.Label(r, text=label, bg=C["card"], fg=C["txt"], font=("Segoe UI", 11), anchor="w").pack(side="left")
            tk.Label(r, text=value, bg=C["card"], fg=color, font=("Segoe UI", 11, "bold"), anchor="e").pack(side="right")

    def pg_search(self):
        self.clr()
        self.hdr(self.t("search"))
        sf = tk.Frame(self.content, bg=C["bg"], padx=20, pady=10)
        sf.pack(fill="x")
        self.srch_e = tk.Entry(sf, font=("Segoe UI", 13), bd=1, relief="solid")
        self.srch_e.pack(side="left", fill="x", expand=True, ipady=8, padx=(0,10))
        self.btn(sf, self.t("search"), self.do_search).pack(side="left")
        self.srch_r = tk.Frame(self.content, bg=C["bg"], padx=20)
        self.srch_r.pack(fill="both", expand=True)
        tk.Label(self.srch_r, text=self.t("type_search"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 12)).pack(pady=40)

    def do_search(self):
        q = self.srch_e.get().strip()
        if not q:
            return
        for w in self.srch_r.winfo_children():
            w.destroy()
        jobs = self.db.get_jobs()
        custs = self.db.get_customers()
        invs = self.db.get_invoices()
        q_lower = q.lower()
        fj = [j for j in jobs if q_lower in (j["job_code"]+j["item"]+(j["problem"] or "")+(j["customer_name"] or "")).lower() or q == str(j["id"])]
        fc = [c for c in custs if q_lower in (c["name"]+(c["phone"] or "")+(c["email"] or "")).lower() or q == str(c["id"])]
        fi = [i for i in invs if q_lower in (i["invoice_code"]+(i["customer_name"] or "")).lower() or q == str(i["id"])]
        t = len(fj)+len(fc)+len(fi)
        if t == 0:
            tk.Label(self.srch_r, text=f"No results for '{q}'", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=40)
            return
        tk.Label(self.srch_r, text=f"{t} result(s) for '{q}'", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=8)
        if fj:
            tk.Label(self.srch_r, text=f"Jobs ({len(fj)})", bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=8)
            for j in fj:
                r = self.row(self.srch_r)
                tk.Label(r, text=f"{j['job_code']} - {j['item']}", bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(side="left")
                tk.Label(r, text=j["status"].upper(), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), padx=10).pack(side="left")
                tk.Label(r, text=f"ID: {j['id']}", bg=C["card"], fg=C["txt3"], font=("Segoe UI", 9), padx=10).pack(side="left")
        if fc:
            tk.Label(self.srch_r, text=f"Customers ({len(fc)})", bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=8)
            for c in fc:
                r = self.row(self.srch_r)
                tk.Label(r, text=c["name"], bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(side="left")
                tk.Label(r, text=c["phone"] or "", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10), padx=10).pack(side="left")
                if c["email"]:
                    tk.Label(r, text=c["email"], bg=C["card"], fg=C["txt3"], font=("Segoe UI", 9), padx=10).pack(side="left")
                tk.Label(r, text=f"ID: {c['id']}", bg=C["card"], fg=C["txt3"], font=("Segoe UI", 9), padx=10).pack(side="left")
        if fi:
            tk.Label(self.srch_r, text=f"Invoices ({len(fi)})", bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=8)
            for i in fi:
                r = self.row(self.srch_r)
                tk.Label(r, text=f"{i['invoice_code']} - RM {i['amount']:.2f}", bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(side="left")
                s = "PAID" if i["paid"] else "UNPAID"
                co = C["ok"] if i["paid"] else C["err"]
                tk.Label(r, text=s, bg=co, fg=C["white"], font=("Segoe UI", 9, "bold"), padx=8, pady=2).pack(side="right")

    def pg_backup(self):
        self.clr()
        self.hdr(self.t("backup"))
        f = tk.Frame(self.content, bg=C["bg"], padx=20)
        f.pack(fill="both", expand=True)
        s1 = self.row(f)
        tk.Label(s1, text="Full Backup (Recommended)", bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(s1, text="Saves all data: customers, jobs, invoices, appointments, settings", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        bf1 = tk.Frame(s1, bg=C["card"])
        bf1.pack(fill="x", pady=5)
        self.btn(bf1, "Backup Now", self.do_backup, bg=C["ok"]).pack(side="left", padx=5)
        self.btn(bf1, "Restore Backup", self.do_restore, bg=C["warn"]).pack(side="left", padx=5)
        s2 = self.row(f)
        tk.Label(s2, text="Export to CSV (for Excel/accounting)", bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        for l, fn, g in [("Customers","customers.csv",lambda:self.db.get_customers()),("Jobs","jobs.csv",lambda:self.db.get_jobs()),("Invoices","invoices.csv",lambda:self.db.get_invoices())]:
            r = tk.Frame(s2, bg=C["card"])
            r.pack(fill="x", pady=3)
            tk.Label(r, text=l, bg=C["card"], fg=C["txt"], font=("Segoe UI", 11), anchor="w").pack(side="left")
            tk.Button(r, text=f"Export {fn}", command=lambda fn=fn,g=g: self.do_export(fn,g), bg=C["pri"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=4, cursor="hand2").pack(side="right")

    def do_backup(self):
        from tkinter import filedialog
        db_path = os.path.join(APP_DIR, "data", "data.db")
        if not os.path.exists(db_path):
            return messagebox.showerror("Error", "No data to backup")
        default_name = f"repairshop_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        fp = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database","*.db")], initialfile=default_name)
        if not fp:
            return
        import shutil
        try:
            shutil.copy2(db_path, fp)
            messagebox.showinfo("Backup Complete", f"Data backed up to:\n{fp}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")

    def do_restore(self):
        from tkinter import filedialog
        fp = filedialog.askopenfilename(filetypes=[("Database","*.db")])
        if not fp:
            return
        if not messagebox.askyesno("Confirm Restore", "This will replace ALL current data with the backup.\n\nAre you sure?"):
            return
        import shutil
        db_path = os.path.join(APP_DIR, "data", "data.db")
        try:
            shutil.copy2(fp, db_path)
            self.db.close()
            self.db = Database(db_path)
            messagebox.showinfo("Restore Complete", "Data restored! App will refresh.")
            self.layout()
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {e}")

    def do_export(self, fn, g):
        from tkinter import filedialog, csv
        data = g()
        if not data:
            return messagebox.showinfo("Info", "Nothing to export")
        fp = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile=fn)
        if not fp:
            return
        try:
            with open(fp, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(data[0].keys())
                for row in data:
                    w.writerow(list(row))
            messagebox.showinfo("Done", f"Exported to {fp}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pg_set(self):
        self.clr()
        self.hdr(self.t("settings"))
        f = tk.Frame(self.content, bg=C["bg"], padx=20)
        f.pack(fill="both", expand=True)
        s = self.row(f)
        tk.Label(s, text=self.t("business_info"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        for l, v, cmd in [("Name", self.db.get_setting("business_name",""), self.edit_biz_name), ("Phone", self.db.get_setting("business_phone",""), self.edit_biz_phone), ("Email", self.db.get_setting("business_email",""), self.edit_biz_email)]:
            r = tk.Frame(s, bg=C["card"])
            r.pack(fill="x", pady=2)
            tk.Label(r, text=f"{self.t(l.lower())}: {v}", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 11)).pack(side="left")
            tk.Button(r, text="Edit", command=cmd, bg=C["card"], fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=8, cursor="hand2").pack(side="right")
        s_gr = self.row(f)
        tk.Label(s_gr, text=self.t("google_review"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(s_gr, text="Add your Google Maps link to invoices", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        gr_val = self.db.get_setting("google_review", "")
        gr_frame = tk.Frame(s_gr, bg=C["card"])
        gr_frame.pack(fill="x", pady=5)
        gr_display = gr_val if gr_val else "Not set"
        tk.Label(gr_frame, text=f"Maps Link: {gr_display}", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 11)).pack(side="left")
        tk.Button(gr_frame, text="Edit", command=self.edit_google_review, bg=C["card"], fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=8, cursor="hand2").pack(side="right")
        tk.Label(s_gr, text="How to get your Google Maps link:", bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10,2))
        tk.Label(s_gr, text="1. Open Google Maps (google.com/maps)", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text="2. Search for your business name", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text="3. Click on your business", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text="4. Click the 'Share' button (under photos)", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text="5. Click 'Copy link' and paste it in Edit above", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text="", bg=C["card"], font=("Segoe UI", 6)).pack()
        tk.Label(s_gr, text="Example link format:", bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5,2))
        tk.Label(s_gr, text="https://maps.google.com/?cid=123456789", bg=C["card"], fg="#2563EB", font=("Segoe UI", 9), anchor="w").pack(fill="x")
        s2 = self.row(f)
        tk.Label(s2, text=self.t("security"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        has = bool(self.db.get_setting("pin_hash"))
        if has:
            tk.Label(s2, text=self.t("pin_active"), bg=C["card"], fg=C["ok"], font=("Segoe UI", 11)).pack(anchor="w", pady=2)
            self.btn(s2, self.t("change_pin"), self.pg_chg_pin).pack(anchor="w", pady=5)
            self.btn(s2, self.t("remove_pin"), self.rm_pin, bg=C["err"]).pack(anchor="w", pady=3)
        else:
            tk.Label(s2, text=self.t("pin_not_set"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 11)).pack(anchor="w", pady=2)
            self.btn(s2, self.t("set_pin"), self.pg_set_pin).pack(anchor="w", pady=5)
        s3 = self.row(f)
        tk.Label(s3, text="Language", bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        lf = tk.Frame(s3, bg=C["card"])
        lf.pack(fill="x", pady=5)
        self.lang_var = tk.StringVar(value=self.lang)
        for v, t in [("en","English"),("ms","Bahasa Malaysia"),("zh","Chinese")]:
            tk.Radiobutton(lf, text=t, variable=self.lang_var, value=v, bg=C["card"], font=("Segoe UI", 11)).pack(side="left", padx=10)
        self.btn(s3, self.t("save"), self.change_lang, bg=C["ok"]).pack(anchor="w", pady=5)
        s_inv = self.row(f)
        tk.Label(s_inv, text="Invoice Format", bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(s_inv, text="Choose how invoices are sent to customers", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        ifr = tk.Frame(s_inv, bg=C["card"])
        ifr.pack(fill="x", pady=5)
        self.inv_fmt_var = tk.StringVar(value=self.db.get_setting("invoice_format", "text"))
        tk.Radiobutton(ifr, text="Text (plain message)", variable=self.inv_fmt_var, value="text", bg=C["card"], font=("Segoe UI", 11)).pack(side="left", padx=10)
        tk.Radiobutton(ifr, text="PDF (professional invoice)", variable=self.inv_fmt_var, value="pdf", bg=C["card"], font=("Segoe UI", 11)).pack(side="left", padx=10)
        self.btn(s_inv, self.t("save"), self.save_inv_fmt, bg=C["ok"]).pack(anchor="w", pady=5)
        s5 = self.row(f)
        tk.Label(s5, text="Startup", bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(s5, text="Open app automatically when Windows starts", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        self.btn(s5, "Toggle Open on Startup", self.toggle_startup, bg=C["warn"]).pack(anchor="w", pady=5)

    def toggle_startup(self):
        startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        shortcut_path = os.path.join(startup_folder, "Kerja Mudah.bat")
        try:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                messagebox.showinfo("Done", "App will no longer open on startup")
            else:
                exe_path = sys.executable if getattr(sys, 'frozen', False) else sys.executable
                bat_content = f'@echo off\nstart "" "{exe_path}"'
                with open(shortcut_path, "w") as f:
                    f.write(bat_content)
                messagebox.showinfo("Done", "App will now open on startup")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update startup: {e}")

    def edit_biz_name(self):
        self._edit_biz_field("business_name", "Business Name")

    def edit_biz_phone(self):
        self._edit_biz_field("business_phone", "Phone Number")

    def edit_biz_email(self):
        self._edit_biz_field("business_email", "Email")

    def edit_google_review(self):
        self._edit_biz_field("google_review", "Google Review Link")

    def _edit_biz_field(self, field, label):
        if self.db.get_setting("pin_hash"):
            self._pending_biz_edit = field
            self._pending_biz_label = label
            self._verify_pin_for_edit()
        else:
            self._show_biz_edit_dialog(field, label)

    def _verify_pin_for_edit(self):
        win = tk.Toplevel(self.root)
        win.title("Verify PIN")
        win.geometry("300x180")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text="Enter PIN to edit", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(pady=15)
        pin_e = tk.Entry(win, font=("Segoe UI", 14), bd=1, relief="solid", width=10, justify="center", show="*")
        pin_e.pack(pady=5)
        pin_e.focus()
        def verify():
            if self.h(pin_e.get().strip()) == self.db.get_setting("pin_hash"):
                win.destroy()
                self._show_biz_edit_dialog(self._pending_biz_edit, self._pending_biz_label)
            else:
                messagebox.showerror("Error", "Wrong PIN")
                pin_e.delete(0, tk.END)
        pin_e.bind("<Return>", lambda e: verify())
        self.btn(win, "Verify", verify).pack(pady=10)

    def _show_biz_edit_dialog(self, field, label):
        win = tk.Toplevel(self.root)
        win.title(f"Edit {label}")
        win.geometry("350x180")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text=f"New {label}:", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(pady=15)
        e = tk.Entry(win, font=("Segoe UI", 14), bd=1, relief="solid", width=25)
        e.insert(0, self.db.get_setting(field, ""))
        e.pack(pady=5)
        e.focus()
        def save():
            val = e.get().strip()
            if not val:
                return messagebox.showerror("Error", "Cannot be empty")
            self.db.set_setting(field, val)
            win.destroy()
            messagebox.showinfo("Done", f"{label} updated!")
            self.pg_set()
        e.bind("<Return>", lambda e: save())
        self.btn(win, "Save", save, bg=C["ok"]).pack(pady=10)

    def pg_set_pin(self):
        self.clr()
        self.hdr(self.t("set_pin"))
        f = tk.Frame(self.content, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        self.sp1 = self.field(f, "PIN (4 digits)")
        self.sp2 = self.field(f, self.t("confirm_pin"))
        bf = tk.Frame(f, bg=C["bg"], pady=20); bf.pack(fill="x")
        self.btn(bf, self.t("save"), self.save_pin).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=self.pg_set, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def save_pin(self):
        p = self.sp1.get().strip()
        c = self.sp2.get().strip()
        if len(p) != 4 or not p.isdigit():
            return messagebox.showerror("Error", "PIN must be 4 digits")
        if p != c:
            return messagebox.showerror("Error", "PINs don't match")
        self.db.set_setting("pin_hash", self.h(p))
        messagebox.showinfo("Done", "PIN set")
        self.pg_set()

    def pg_chg_pin(self):
        self.clr()
        self.hdr(self.t("change_pin"))
        f = tk.Frame(self.content, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        self.cp1 = self.field(f, "Current PIN")
        self.cp2 = self.field(f, "New PIN")
        self.cp3 = self.field(f, "Confirm New PIN")
        bf = tk.Frame(f, bg=C["bg"], pady=20); bf.pack(fill="x")
        self.btn(bf, self.t("save"), self.save_chg_pin).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=self.pg_set, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def save_chg_pin(self):
        o = self.cp1.get().strip()
        n = self.cp2.get().strip()
        c = self.cp3.get().strip()
        if self.h(o) != self.db.get_setting("pin_hash"):
            return messagebox.showerror("Error", "Wrong current PIN")
        if len(n) != 4 or not n.isdigit():
            return messagebox.showerror("Error", "New PIN must be 4 digits")
        if n != c:
            return messagebox.showerror("Error", "PINs don't match")
        self.db.set_setting("pin_hash", self.h(n))
        messagebox.showinfo("Done", "PIN changed")
        self.pg_set()

    def rm_pin(self):
        if messagebox.askyesno("Confirm", "Remove PIN?"):
            self.db.conn.execute("DELETE FROM settings WHERE key = 'pin_hash'")
            self.db.conn.commit()
            messagebox.showinfo("Done", "PIN removed")
            self.pg_set()

    def save_inv_fmt(self):
        fmt = self.inv_fmt_var.get()
        self.db.set_setting("invoice_format", fmt)
        messagebox.showinfo("Done", f"Invoice format set to: {fmt.upper()}")
        self.pg_set()

    def change_lang(self):
        if getattr(self, '_changing_lang', False):
            return
        self._changing_lang = True
        self.lang = self.lang_var.get()
        self.db.set_setting("language", self.lang)
        self.root.title(self.t("app_title"))
        self.root.after(10, self._do_lang_change)

    def _do_lang_change(self):
        self.layout()
        self._changing_lang = False

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _on_close(self):
        self.db.close()
        self.root.destroy()

if __name__ == "__main__":
    App().run()
