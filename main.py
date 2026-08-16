import tkinter as tk
from tkinter import ttk, messagebox
import os, sys, hashlib, webbrowser, urllib.parse, platform, uuid, time, subprocess
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
    except (ValueError, TypeError):
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
        "outstanding": "Outstanding", "jobs_done": "Jobs Done (This Month)",
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
        "google_review_hint": "Paste your Google Maps business link",
        "leave_review": "We'd love your feedback!",
        "rate_us": "Leave us a Google review",
        "pending": "Pending", "in_progress": "In Progress", "status": "Status",
        "edit": "Edit", "pdf": "PDF", "send_reminder": "Send Reminder",
        "activate": "Activate", "try_demo": "Try Demo (7 days)", "copy": "Copy",
        "license_activation": "License Activation Required",
        "enter_license_key": "Enter your license key to activate",
        "your_hwid": "Your Hardware ID (send this to get a key):",
        "demo_mode": "Demo mode: limited to 10 jobs, 7 day trial",
        "contact_seller": "Contact seller to get your license key",
        "demo_expired": "Your 7-day demo has expired. Please activate with a license key to continue.",
        "demo_limit": "Demo mode is limited to 10 jobs. Please activate with a license key.",
        "activated": "License activated! You can now use the full app.",
        "invalid_key": "This license key is not valid.",
        "hwid_copied": "HWID copied to clipboard!",
        "pickup_reminders": "Pickup Reminders",
        "waiting_for_pickup": "Waiting for Pickup",
        "waiting": "Waiting",
        "days_unit": "day(s)",
        "ready": "Ready",
        "code": "Code",
        "action": "Action",
        "or_pick": "Or pick:",
        "edit_job": "Edit Job",
        "edit_customer": "Edit Customer",
        "edit_appointment": "Edit Appointment",
        "job_complete_msg": "Job Complete!",
        "invoice_already_exists": "(Invoice already exists)",
        "language": "Language",
        "invoice_format": "Invoice Format",
        "choose_format": "Choose how invoices are sent to customers",
        "text_plain": "Text (plain message)",
        "pdf_professional": "PDF (professional invoice)",
        "startup": "Startup",
        "open_on_startup": "Open app automatically when Windows starts",
        "toggle_startup": "Toggle Open on Startup",
        "maps_link": "Maps Link",
        "add_google_maps": "Add your Google Maps link to invoices",
        "enter_pin_to_edit": "Enter PIN to edit",
        "new_label": "New",
        "current_pin": "Current PIN",
        "new_pin": "New PIN",
        "confirm_new_pin": "Confirm New PIN",
        "pin_4_digits": "PIN (4 digits)",
        "summary": "Summary",
        "total_earned": "Total Earned (All Time)",
        "outstanding_unpaid": "Outstanding (Unpaid)",
        "total_jobs": "Total Jobs",
        "completed_jobs": "Completed Jobs",
        "active_jobs_count": "Active Jobs",
        "total_customers": "Total Customers",
        "paid_invoices_count": "Paid Invoices",
        "unpaid_invoices_count": "Unpaid Invoices",
        "revenue_today": "Revenue Today",
        "revenue_week": "Revenue This Week",
        "revenue_month": "Revenue This Month",
        "revenue_outstanding": "Outstanding",
        "money_today": "Money collected today",
        "money_week": "Money collected this week",
        "money_month": "Money collected this month",
        "money_owed": "Still owed by customers",
        "invoices": "invoices",
        "total": "total",
        "unknown": "Unknown",
        "no_phone": "No phone number for this customer.",
        "no_email": "No email found for this customer. Add email to customer first.",
        "no_phone_short": "No Phone",
        "no_email_short": "No Email",
        "confirm_restore": "Confirm Restore",
        "restore_warning": "This will replace ALL current data with the backup. Are you sure?",
        "confirm": "Confirm",
        "remove_pin_confirm": "Remove PIN?",
        "cleanup": "Cleanup",
        "cleanup_msg": "old paid invoice(s) older than 7 days.",
        "cleanup_apts_msg": "past appointment(s) automatically removed.",
        "backup_complete": "Backup Complete",
        "restore_complete": "Data restored! App will refresh.",
        "nothing_export": "Nothing to export",
        "exported": "Exported to",
        "full_backup": "Full Backup (Recommended)",
        "backup_desc": "Saves all data: customers, jobs, invoices, appointments, settings",
        "backup_now": "Backup Now",
        "restore_backup": "Restore Backup",
        "export_csv_section": "Export to CSV (for Excel/accounting)",
        "customers_csv": "Customers",
        "jobs_csv": "Jobs",
        "invoices_csv": "Invoices",
        "export": "Export",
        "pdf_error": "PDF Error",
        "pdf_failed": "Failed to generate PDF",
        "whatsapp_opened": "WhatsApp opened for",
        "email_opened": "Email opened for",
        "opening_email": "Opening email client for",
        "opening_whatsapp": "Opening WhatsApp for",
        "invoice_created": "Invoice created!",
        "pdf_saved": "Invoice PDF saved to:",
        "pdf_opened": "PDF invoice opened. Drag it into WhatsApp to send.",
        "job_saved": "Job saved",
        "job_updated": "Job updated",
        "customer_updated": "Customer updated",
        "customer_saved": "Customer saved",
        "appointment_updated": "Appointment updated",
        "appointment_saved": "Appointment saved",
        "pin_set": "PIN set",
        "pin_changed": "PIN changed",
        "pin_removed": "PIN removed",
        "enter_business_name": "Enter business name",
        "enter_item": "Enter item",
        "enter_name": "Enter name",
        "quote_number": "Quote must be a number",
        "cannot_empty": "Cannot be empty",
        "pin_digits": "PIN must be 4 digits",
        "pins_match": "PINs don't match",
        "wrong_current_pin": "Wrong current PIN",
        "new_pin_digits": "New PIN must be 4 digits",
        "startup_updated": "App will now open on startup",
        "startup_removed": "App will no longer open on startup",
        "startup_error": "Could not update startup",
        "no_backup": "No data to backup",
        "backup_failed": "Backup failed",
        "restore_failed": "Restore failed",
        "invoice_format_set": "Invoice format set to:",
        "remove_pin_msg": "PIN removed",
        "label_updated": "updated!",
        "invoice_title": "Invoice Title",
        "payment_terms": "Payment Terms",
        "thank_you_note": "Thank You Note",
        "footer_text": "Footer Text",
        "preview_invoice": "Preview Invoice",
        "invoice_parameters": "Invoice Parameters",
        "customize_invoice": "Customize invoice text and footer",
        "search_jobs": "Search jobs...",
        "search_customers": "Search customers...",
        "search_appointments": "Search appointments...",
        "search_invoices": "Search invoices...",
        "waiting_for_pickup_count": "Waiting for Pickup",
        "send_reminder": "Send Reminder",
        "or_pick": "Or pick:",
        "edit_job_title": "Edit Job",
        "edit_customer_title": "Edit Customer",
        "edit_appointment_title": "Edit Appointment",
        "job_complete_title": "Job Complete!",
        "invoice_already_exists": "(Invoice already exists)",
        "invoice_whatsapp": "Invoice + WhatsApp",
        "invoice_email": "Invoice + Email",
        "just_invoice": "Just Invoice",
        "skip": "Skip",
        "create": "Create",
        "confirm_restore_title": "Confirm Restore",
        "confirm_restore_msg": "This will replace ALL current data with the backup.\n\nAre you sure?",
        "full_backup": "Full Backup (Recommended)",
        "backup_desc": "Saves all data: customers, jobs, invoices, appointments, settings",
        "backup_now": "Backup Now",
        "restore_backup": "Restore Backup",
        "export_csv_section": "Export to CSV (for Excel/accounting)",
        "export_customers": "Export customers.csv",
        "export_jobs": "Export jobs.csv",
        "export_invoices": "Export invoices.csv",
        "revenue_today": "Revenue Today",
        "revenue_week": "Revenue This Week",
        "revenue_month": "Revenue This Month",
        "outstanding": "Outstanding",
        "summary": "Summary",
        "total_earned": "Total Earned (All Time)",
        "outstanding_unpaid": "Outstanding (Unpaid)",
        "total_jobs": "Total Jobs",
        "completed_jobs": "Completed Jobs",
        "active_jobs_count": "Active Jobs",
        "total_customers": "Total Customers",
        "paid_invoices_count": "Paid Invoices",
        "unpaid_invoices_count": "Unpaid Invoices",
        "language": "Language",
        "invoice_format": "Invoice Format",
        "choose_format": "Choose how invoices are sent to customers",
        "text_plain": "Text (plain message)",
        "pdf_professional": "PDF (professional invoice)",
        "preview_invoice": "Preview Invoice",
        "startup": "Startup",
        "open_on_startup": "Open app automatically when Windows starts",
        "toggle_startup": "Toggle Open on Startup",
        "invoice_parameters": "Invoice Parameters",
        "customize_invoice": "Customize invoice text and footer",
        "invoice_title": "Invoice Title",
        "payment_terms": "Payment Terms",
        "thank_you_note": "Thank You Note",
        "footer_text": "Footer Text",
        "bill_to": "Bill To:",
        "total": "Total:",
        "status": "Status",
        "unpaid_status": "UNPAID",
        "paid_status": "PAID",
        "close": "Close",
        "verify": "Verify",
        "enter_pin_to_edit": "Enter PIN to edit",
        "new_prefix": "New",
        "maps_link_label": "Maps Link:",
        "add_google_maps": "Add your Google Maps link to invoices",
        "google_maps_instructions": "How to get your Google Maps link:",
        "google_maps_step1": "1. Open Google Maps (google.com/maps)",
        "google_maps_step2": "2. Search for your business name",
        "google_maps_step3": "3. Click on your business",
        "google_maps_step4": "4. Click the 'Share' button (under photos)",
        "google_maps_step5": "5. Click 'Copy link' and paste it in Edit above",
        "example_link": "Example link format:",
        "no_results_for": "No results for",
        "results_count": "result(s) for",
        "jobs_header": "Jobs",
        "customers_header": "Customers",
        "invoices_header": "Invoices",
        "id_label": "ID:",
        "optional_fields_hint": "Phone, Email, and Google Review are optional - you can add them later in Settings",
        "today": "Today",
        "this_week": "This Week",
        "this_month": "This Month",
        "owed": "Owed",
        "collected_today": "Collected today",
        "collected_week": "Collected this week",
        "collected_month": "Collected this month",
        "owed_desc": "Still owed",
        "method": "Method",
        "mon": "Mon", "tue": "Tue", "wed": "Wed", "thu": "Thu", "fri": "Fri", "sat": "Sat", "sun": "Sun",
        "pick_date": "Pick Date", "today_btn": "Today", "pick_btn": "Pick",
        "show": "Show", "hide": "Hide",
        "demo_bar": "DEMO MODE - {days} days remaining | Activate with license key",
        "waiting_fmt": "Waiting {count} day(s)",
        "walk_in": "Walk-in", "customer_fallback": "Customer",
        "service_label": "Service:", "ready_since": "Ready since:",
        "due_date_label": "Due Date:", "amount_label": "Amount:",
        "please_pickup": "Please pick up at your convenience.",
        "invoice_label": "Invoice:", "amount_col": "Amount",
        "payment_title": "Payment",
        "not_set": "Not set",
        "on_startup": "ON - App will start with Windows",
        "off_startup": "OFF - App will not start with Windows",
        "empty_placeholder": "(empty)",
        "format_label": "Format:", "phone_label": "Phone:", "email_label": "Email:",
        "walk_in_customer": "Walk-in Customer",
        "leave_review_label": "Leave us a Google review:",
        "google_review_link": "Google Review Link:",
        "no_method": "No method",
        "updated_suffix": "updated!",
        "maps_link_paste": "Paste your Google Maps business link:",
        "invalid_google_link": "Invalid Google review link.\n\nPlease copy the link from Google Maps:\n1. Search your business on Google Maps\n2. Click 'Share' or 'Write a review'\n3. Copy the link and paste here",
        "item_label": "Item", "service_problem": "Service / Problem",
        "wa": "WA",
    },
    "ms": {
        "app_title": "Kerja Mudah",
        "home": "Utama", "jobs": "Kerja", "customers": "Pelanggan",
        "appointments": "Temujanji", "invoices": "Invois",
        "reports": "Laporan", "search": "Carian", "backup": "Sandaran", "settings": "Tetapan",
        "dashboard": "Papan Pemuka", "active_jobs": "Kerja Aktif", "today": "Hari Ini",
        "outstanding": "Belum Dibayar", "jobs_done": "Kerja Selesai (Bulan Ini)",
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
        "google_review_hint": "Tampal pautan Google Maps perniagaan anda",
        "leave_review": "Kami menghargai maklum balas anda!",
        "rate_us": "Tinggalkan Google review untuk kami",
        "pending": "Menunggu", "in_progress": "Sedang Dijalankan", "status": "Status",
        "edit": "Sunting", "pdf": "PDF", "send_reminder": "Hantar Peringatan",
        "activate": "Aktifkan", "try_demo": "Cuba Demo (7 hari)", "copy": "Salin",
        "license_activation": "Pengaktifan Lesen Diperlukan",
        "enter_license_key": "Masukkan kunci lesen untuk mengaktifkan",
        "your_hwid": "ID Perkakasan Anda (hantar ini untuk dapat kunci):",
        "demo_mode": "Mod demo: terhad kepada 10 kerja, percubaan 7 hari",
        "contact_seller": "Hubungi penjual untuk dapat kunci lesen",
        "demo_expired": "Demo 7 hari anda telah tamat. Sila aktifkan dengan kunci lesen.",
        "demo_limit": "Mod demo terhad kepada 10 kerja. Sila aktifkan dengan kunci lesen.",
        "activated": "Lesen berjaya diaktifkan! Anda boleh guna app penuh.",
        "invalid_key": "Kunci lesen ini tidak sah.",
        "hwid_copied": "HWID disalin ke papan klip!",
        "pickup_reminders": "Peringatan Pengambilan",
        "waiting_for_pickup": "Menunggu Pengambilan",
        "waiting": "Menunggu",
        "days_unit": "hari",
        "ready": "Sedia",
        "code": "Kod",
        "action": "Tindakan",
        "or_pick": "Atau pilih:",
        "edit_job": "Sunting Kerja",
        "edit_customer": "Sunting Pelanggan",
        "edit_appointment": "Sunting Temujanji",
        "job_complete_msg": "Kerja Selesai!",
        "invoice_already_exists": "(Invois sudah wujud)",
        "language": "Bahasa",
        "invoice_format": "Format Invois",
        "choose_format": "Pilih cara invois dihantar kepada pelanggan",
        "text_plain": "Teks (mesej biasa)",
        "pdf_professional": "PDF (invois profesional)",
        "startup": "Permulaan",
        "open_on_startup": "Buka app secara automatik apabila Windows bermula",
        "toggle_startup": "Tukar Buka pada Permulaan",
        "maps_link": "Pautan Peta",
        "add_google_maps": "Tambah pautan Google Maps anda pada invois",
        "enter_pin_to_edit": "Masukkan PIN untuk menyunting",
        "new_label": "Baru",
        "current_pin": "PIN Semasa",
        "new_pin": "PIN Baru",
        "confirm_new_pin": "Sahkan PIN Baru",
        "pin_4_digits": "PIN (4 digit)",
        "summary": "Ringkasan",
        "total_earned": "Jumlah Diperoleh (Semua Masa)",
        "outstanding_unpaid": "Belum Dibayar",
        "total_jobs": "Jumlah Kerja",
        "completed_jobs": "Kerja Selesai",
        "active_jobs_count": "Kerja Aktif",
        "total_customers": "Jumlah Pelanggan",
        "paid_invoices_count": "Invois Dibayar",
        "unpaid_invoices_count": "Invois Belum Dibayar",
        "revenue_today": "Pendapatan Hari Ini",
        "revenue_week": "Pendapatan Minggu Ini",
        "revenue_month": "Pendapatan Bulan Ini",
        "revenue_outstanding": "Belum Dibayar",
        "money_today": "Wang dikumpul hari ini",
        "money_week": "Wang dikumpul minggu ini",
        "money_month": "Wang dikumpul bulan ini",
        "money_owed": "Masih berhutang oleh pelanggan",
        "invoices": "invois",
        "total": "jumlah",
        "unknown": "Tidak Diketahui",
        "no_phone": "Tiada nombor telefon untuk pelanggan ini.",
        "no_email": "Tiada emel ditemui untuk pelanggan ini. Tambah emel kepada pelanggan dahulu.",
        "no_phone_short": "Tiada Telefon",
        "no_email_short": "Tiada Emel",
        "confirm_restore": "Sahkan Pemulihan",
        "restore_warning": "Ini akan menggantikan SEMUA data semula dengan sandaran. Anda pasti?",
        "confirm": "Sahkan",
        "remove_pin_confirm": "Buang PIN?",
        "cleanup": "Pembersihan",
        "cleanup_msg": "invois lama yang telah dibayar lebih 7 hari.",
        "cleanup_apts_msg": "temujanji lepas telah dipadam secara automatik.",
        "backup_complete": "Sandaran Selesai",
        "restore_complete": "Data dipulihkan! App akan segar semula.",
        "nothing_export": "Tiada data untuk dieksport",
        "exported": "Dieksport ke",
        "full_backup": "Sandaran Penuh (Disyorkan)",
        "backup_desc": "Simpan semua data: pelanggan, kerja, invois, temujanji, tetapan",
        "backup_now": "Sandar Sekarang",
        "restore_backup": "Pulihkan Sandaran",
        "export_csv_section": "Eksport ke CSV (untuk Excel/akaun)",
        "customers_csv": "Pelanggan",
        "jobs_csv": "Kerja",
        "invoices_csv": "Invois",
        "export": "Eksport",
        "pdf_error": "Ralat PDF",
        "pdf_failed": "Gagal menjana PDF",
        "whatsapp_opened": "WhatsApp dibuka untuk",
        "email_opened": "Emel dibuka untuk",
        "opening_email": "Membuka klien emel untuk",
        "opening_whatsapp": "Membuka WhatsApp untuk",
        "invoice_created": "Invois dicipta!",
        "pdf_saved": "PDF invois disimpan ke:",
        "pdf_opened": "PDF invois dibuka. Seret ke WhatsApp untuk hantar.",
        "job_saved": "Kerja disimpan",
        "job_updated": "Kerja dikemaskini",
        "customer_updated": "Pelanggan dikemaskini",
        "customer_saved": "Pelanggan disimpan",
        "appointment_updated": "Temujanji dikemaskini",
        "appointment_saved": "Temujanji disimpan",
        "pin_set": "PIN ditetapkan",
        "pin_changed": "PIN ditukar",
        "pin_removed": "PIN dibuang",
        "enter_business_name": "Masukkan nama perniagaan",
        "enter_item": "Masukkan barang",
        "enter_name": "Masukkan nama",
        "quote_number": "Sebut harga mesti nombor",
        "cannot_empty": "Tidak boleh kosong",
        "pin_digits": "PIN mesti 4 digit",
        "pins_match": "PIN tidak sepadan",
        "wrong_current_pin": "PIN semasa salah",
        "new_pin_digits": "PIN Baru mesti 4 digit",
        "startup_updated": "App akan dibuka pada permulaan",
        "startup_removed": "App tidak akan dibuka pada permulaan lagi",
        "startup_error": "Tidak dapat mengemas kini permulaan",
        "no_backup": "Tiada data untuk disandar",
        "backup_failed": "Sandaran gagal",
        "restore_failed": "Pemulihan gagal",
        "invoice_format_set": "Format invois ditetapkan kepada:",
        "remove_pin_msg": "PIN dibuang",
        "label_updated": "berjaya dikemaskini!",
        "invoice_title": "Tajuk Invois",
        "payment_terms": "Syarat Pembayaran",
        "thank_you_note": "Nota Terima Kasih",
        "footer_text": "Teks Kaki",
        "preview_invoice": "Pratonton Invois",
        "invoice_parameters": "Parameter Invois",
        "customize_invoice": "Suaikan teks invois dan kaki",
        "search_jobs": "Carian kerja...",
        "search_customers": "Carian pelanggan...",
        "search_appointments": "Carian temujanji...",
        "search_invoices": "Carian invois...",
        "waiting_for_pickup_count": "Menunggu Pengambilan",
        "send_reminder": "Hantar Peringatan",
        "or_pick": "Atau pilih:",
        "edit_job_title": "Sunting Kerja",
        "edit_customer_title": "Sunting Pelanggan",
        "edit_appointment_title": "Sunting Temujanji",
        "job_complete_title": "Kerja Selesai!",
        "invoice_already_exists": "(Invois sudah wujud)",
        "invoice_whatsapp": "Invois + WhatsApp",
        "invoice_email": "Invois + Emel",
        "just_invoice": "Invois Sahaja",
        "skip": "Langkau",
        "create": "Cipta",
        "confirm_restore_title": "Sahkan Pemulihan",
        "confirm_restore_msg": "Ini akan menggantikan SEMUA data semula dengan sandaran. Anda pasti?",
        "full_backup": "Sandaran Penuh (Disyorkan)",
        "backup_desc": "Simpan semua data: pelanggan, kerja, invois, temujanji, tetapan",
        "backup_now": "Sandar Sekarang",
        "restore_backup": "Pulihkan Sandaran",
        "export_csv_section": "Eksport ke CSV (untuk Excel/akaun)",
        "export_customers": "Eksport customers.csv",
        "export_jobs": "Eksport jobs.csv",
        "export_invoices": "Eksport invoices.csv",
        "revenue_today": "Pendapatan Hari Ini",
        "revenue_week": "Pendapatan Minggu Ini",
        "revenue_month": "Pendapatan Bulan Ini",
        "outstanding": "Belum Dibayar",
        "summary": "Ringkasan",
        "total_earned": "Jumlah Diperoleh (Semua Masa)",
        "outstanding_unpaid": "Belum Dibayar",
        "total_jobs": "Jumlah Kerja",
        "completed_jobs": "Kerja Selesai",
        "active_jobs_count": "Kerja Aktif",
        "total_customers": "Jumlah Pelanggan",
        "paid_invoices_count": "Invois Dibayar",
        "unpaid_invoices_count": "Invois Belum Dibayar",
        "language": "Bahasa",
        "invoice_format": "Format Invois",
        "choose_format": "Pilih cara invois dihantar kepada pelanggan",
        "text_plain": "Teks (mesej biasa)",
        "pdf_professional": "PDF (invois profesional)",
        "preview_invoice": "Pratonton Invois",
        "startup": "Permulaan",
        "open_on_startup": "Buka app secara automatik apabila Windows bermula",
        "toggle_startup": "Tukar Buka pada Permulaan",
        "invoice_parameters": "Parameter Invois",
        "customize_invoice": "Suaikan teks invois dan kaki",
        "invoice_title": "Tajuk Invois",
        "payment_terms": "Syarat Pembayaran",
        "thank_you_note": "Nota Terima Kasih",
        "footer_text": "Teks Kaki",
        "bill_to": "Bil Kepada:",
        "total": "Jumlah:",
        "status": "Status",
        "unpaid_status": "BELUM DIBAYAR",
        "paid_status": "DIBAYAR",
        "close": "Tutup",
        "verify": "Sahkan",
        "enter_pin_to_edit": "Masukkan PIN untuk menyunting",
        "new_prefix": "Baru",
        "maps_link_label": "Pautan Peta:",
        "add_google_maps": "Tambah pautan Google Maps anda pada invois",
        "google_maps_instructions": "Cara dapat pautan Google Maps anda:",
        "google_maps_step1": "1. Buka Google Maps (google.com/maps)",
        "google_maps_step2": "2. Cari nama perniagaan anda",
        "google_maps_step3": "3. Klik pada perniagaan anda",
        "google_maps_step4": "4. Klik butang 'Share' (di bawah foto)",
        "google_maps_step5": "5. Klik 'Copy link' dan tampal di Edit di atas",
        "example_link": "Contoh format pautan:",
        "no_results_for": "Tiada hasil untuk",
        "results_count": "hasil untuk",
        "jobs_header": "Kerja",
        "customers_header": "Pelanggan",
        "invoices_header": "Invois",
        "id_label": "ID:",
        "optional_fields_hint": "Telefon, Emel, dan Google Review adalah pilihan - anda boleh tambah kemudian dalam Tetapan",
        "today": "Hari Ini",
        "this_week": "Minggu Ini",
        "this_month": "Bulan Ini",
        "owed": "Hutang",
        "collected_today": "Dikumpul hari ini",
        "collected_week": "Dikumpul minggu ini",
        "collected_month": "Dikumpul bulan ini",
        "owed_desc": "Masih berhutang",
        "method": "Kaedah",
        "mon": "Isn", "tue": "Sel", "wed": "Rab", "thu": "Kha", "fri": "Jum", "sat": "Sab", "sun": "Ahd",
        "pick_date": "Pilih Tarikh", "today_btn": "Hari Ini", "pick_btn": "Pilih",
        "show": "Tunjuk", "hide": "Sembunyi",
        "demo_bar": "MOD DEMO - {days} hari lagi | Aktifkan dengan kunci lesen",
        "waiting_fmt": "Menunggu {count} hari",
        "walk_in": "Walk-in", "customer_fallback": "Pelanggan",
        "service_label": "Perkhidmatan:", "ready_since": "Sedia sejak:",
        "due_date_label": "Tarikh Akhir:", "amount_label": "Jumlah:",
        "please_pickup": "Sila ambil pada bila-bila masa yang sesuai.",
        "invoice_label": "Invois:", "amount_col": "Jumlah",
        "payment_title": "Pembayaran",
        "not_set": "Belum ditetapkan",
        "on_startup": "ON - App akan mula bersama Windows",
        "off_startup": "OFF - App tidak akan mula bersama Windows",
        "empty_placeholder": "(kosong)",
        "format_label": "Format:", "phone_label": "Telefon:", "email_label": "Emel:",
        "walk_in_customer": "Pelanggan Walk-in",
        "leave_review_label": "Tinggalkan Google review untuk kami:",
        "google_review_link": "Pautan Google Review:",
        "no_method": "Tiada kaedah",
        "updated_suffix": "berjaya dikemaskini!",
        "maps_link_paste": "Tampal pautan Google Maps perniagaan anda:",
        "invalid_google_link": "Pautan Google review tidak sah.\n\nSila salin pautan dari Google Maps:\n1. Cari perniagaan anda di Google Maps\n2. Klik 'Share' atau 'Write a review'\n3. Salin pautan dan tampal di sini",
        "item_label": "Barang", "service_problem": "Perkhidmatan / Masalah",
        "wa": "WA",
    },
    "zh": {
        "app_title": "Kerja Mudah",
        "home": "主页", "jobs": "工作", "customers": "客户",
        "appointments": "预约", "invoices": "发票",
        "reports": "报告", "search": "搜索", "backup": "备份", "settings": "设置",
        "dashboard": "仪表板", "active_jobs": "进行中", "today": "今天",
        "outstanding": "未收款", "jobs_done": "已完成 (本月)",
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
        "google_review_hint": "粘贴您的Google Maps商家链接",
        "leave_review": "我们期待您的反馈！",
        "rate_us": "请给我们留个Google评价",
        "pending": "待处理", "in_progress": "进行中", "status": "状态",
        "edit": "编辑", "pdf": "PDF", "send_reminder": "发送提醒",
        "activate": "激活", "try_demo": "试用演示 (7天)", "copy": "复制",
        "license_activation": "需要激活许可证",
        "enter_license_key": "输入许可证密钥以激活",
        "your_hwid": "您的硬件ID（发送此码获取密钥）：",
        "demo_mode": "演示模式：限10个工作，7天试用",
        "contact_seller": "联系卖家获取许可证密钥",
        "demo_expired": "您的7天演示已过期。请使用许可证密钥激活。",
        "demo_limit": "演示模式限10个工作。请使用许可证密钥激活。",
        "activated": "许可证已激活！您现在可以使用完整应用。",
        "invalid_key": "此许可证密钥无效。",
        "hwid_copied": "HWID已复制到剪贴板！",
        "pickup_reminders": "取件提醒",
        "waiting_for_pickup": "等待取件",
        "waiting": "等待中",
        "days_unit": "天",
        "ready": "已准备好",
        "code": "编号",
        "action": "操作",
        "or_pick": "或选择：",
        "edit_job": "编辑工作",
        "edit_customer": "编辑客户",
        "edit_appointment": "编辑预约",
        "job_complete_msg": "工作完成！",
        "invoice_already_exists": "（发票已存在）",
        "language": "语言",
        "invoice_format": "发票格式",
        "choose_format": "选择发票发送给客户的方式",
        "text_plain": "文本（纯消息）",
        "pdf_professional": "PDF（专业发票）",
        "startup": "启动",
        "open_on_startup": "Windows启动时自动打开应用",
        "toggle_startup": "切换启动时打开",
        "maps_link": "地图链接",
        "add_google_maps": "将您的Google Maps链接添加到发票",
        "enter_pin_to_edit": "输入PIN以编辑",
        "new_label": "新",
        "current_pin": "当前PIN",
        "new_pin": "新PIN",
        "confirm_new_pin": "确认新PIN",
        "pin_4_digits": "PIN（4位数字）",
        "summary": "摘要",
        "total_earned": "总收入（全部）",
        "outstanding_unpaid": "未收款",
        "total_jobs": "总工作数",
        "completed_jobs": "已完成工作",
        "active_jobs_count": "进行中工作",
        "total_customers": "总客户数",
        "paid_invoices_count": "已付发票",
        "unpaid_invoices_count": "未付发票",
        "revenue_today": "今日收入",
        "revenue_week": "本周收入",
        "revenue_month": "本月收入",
        "revenue_outstanding": "未收款",
        "money_today": "今日收款",
        "money_week": "本周收款",
        "money_month": "本月收款",
        "money_owed": "客户欠款",
        "invoices": "张发票",
        "total": "合计",
        "unknown": "未知",
        "no_phone": "此客户没有电话号码。",
        "no_email": "未找到此客户的电子邮件。请先添加邮箱。",
        "no_phone_short": "无电话",
        "no_email_short": "无邮箱",
        "confirm_restore": "确认恢复",
        "restore_warning": "这将用备份替换所有当前数据。确定吗？",
        "confirm": "确认",
        "remove_pin_confirm": "删除PIN？",
        "cleanup": "清理",
        "cleanup_msg": "超过7天的已付款旧发票。",
        "cleanup_apts_msg": "已过期的预约已自动删除。",
        "backup_complete": "备份完成",
        "restore_complete": "数据已恢复！应用将刷新。",
        "nothing_export": "没有可导出的数据",
        "exported": "已导出到",
        "full_backup": "完整备份（推荐）",
        "backup_desc": "保存所有数据：客户、工作、发票、预约、设置",
        "backup_now": "立即备份",
        "restore_backup": "恢复备份",
        "export_csv_section": "导出CSV（用于Excel/会计）",
        "customers_csv": "客户",
        "jobs_csv": "工作",
        "invoices_csv": "发票",
        "export": "导出",
        "pdf_error": "PDF错误",
        "pdf_failed": "生成PDF失败",
        "whatsapp_opened": "WhatsApp已打开",
        "email_opened": "邮件已打开",
        "opening_email": "正在打开邮件客户端",
        "opening_whatsapp": "正在打开WhatsApp",
        "invoice_created": "发票已创建！",
        "pdf_saved": "发票PDF已保存到：",
        "pdf_opened": "PDF发票已打开。拖入WhatsApp发送。",
        "job_saved": "工作已保存",
        "job_updated": "工作已更新",
        "customer_updated": "客户已更新",
        "customer_saved": "客户已保存",
        "appointment_updated": "预约已更新",
        "appointment_saved": "预约已保存",
        "pin_set": "PIN已设置",
        "pin_changed": "PIN已更改",
        "pin_removed": "PIN已删除",
        "enter_business_name": "请输入商家名称",
        "enter_item": "请输入物品",
        "enter_name": "请输入姓名",
        "quote_number": "报价必须是数字",
        "cannot_empty": "不能为空",
        "pin_digits": "PIN必须是4位数字",
        "pins_match": "PIN不匹配",
        "wrong_current_pin": "当前PIN错误",
        "new_pin_digits": "新PIN必须是4位数字",
        "startup_updated": "应用将在启动时打开",
        "startup_removed": "应用将不再在启动时打开",
        "startup_error": "无法更新启动设置",
        "no_backup": "没有可备份的数据",
        "backup_failed": "备份失败",
        "restore_failed": "恢复失败",
        "invoice_format_set": "发票格式设置为：",
        "remove_pin_msg": "PIN已删除",
        "label_updated": "已更新！",
        "invoice_title": "发票标题",
        "payment_terms": "付款条款",
        "thank_you_note": "感谢语",
        "footer_text": "页脚文本",
        "preview_invoice": "预览发票",
        "invoice_parameters": "发票参数",
        "customize_invoice": "自定义发票文本和页脚",
        "search_jobs": "搜索工作...",
        "search_customers": "搜索客户...",
        "search_appointments": "搜索预约...",
        "search_invoices": "搜索发票...",
        "waiting_for_pickup_count": "等待取件",
        "send_reminder": "发送提醒",
        "or_pick": "或选择：",
        "edit_job_title": "编辑工作",
        "edit_customer_title": "编辑客户",
        "edit_appointment_title": "编辑预约",
        "job_complete_title": "工作完成！",
        "invoice_already_exists": "（发票已存在）",
        "invoice_whatsapp": "发票 + WhatsApp",
        "invoice_email": "发票 + 电邮",
        "just_invoice": "仅发票",
        "skip": "跳过",
        "create": "创建",
        "confirm_restore_title": "确认恢复",
        "confirm_restore_msg": "这将用备份替换所有当前数据。确定吗？",
        "full_backup": "完整备份（推荐）",
        "backup_desc": "保存所有数据：客户、工作、发票、预约、设置",
        "backup_now": "立即备份",
        "restore_backup": "恢复备份",
        "export_csv_section": "导出CSV（用于Excel/会计）",
        "export_customers": "导出customers.csv",
        "export_jobs": "导出jobs.csv",
        "export_invoices": "导出invoices.csv",
        "revenue_today": "今日收入",
        "revenue_week": "本周收入",
        "revenue_month": "本月收入",
        "outstanding": "未收款",
        "summary": "摘要",
        "total_earned": "总收入（全部）",
        "outstanding_unpaid": "未收款",
        "total_jobs": "总工作数",
        "completed_jobs": "已完成工作",
        "active_jobs_count": "进行中工作",
        "total_customers": "总客户数",
        "paid_invoices_count": "已付发票",
        "unpaid_invoices_count": "未付发票",
        "language": "语言",
        "invoice_format": "发票格式",
        "choose_format": "选择发票发送给客户的方式",
        "text_plain": "文本（纯消息）",
        "pdf_professional": "PDF（专业发票）",
        "preview_invoice": "预览发票",
        "startup": "启动",
        "open_on_startup": "Windows启动时自动打开应用",
        "toggle_startup": "切换启动时打开",
        "invoice_parameters": "发票参数",
        "customize_invoice": "自定义发票文本和页脚",
        "invoice_title": "发票标题",
        "payment_terms": "付款条款",
        "thank_you_note": "感谢语",
        "footer_text": "页脚文本",
        "bill_to": "收款方：",
        "total": "合计：",
        "status": "状态",
        "unpaid_status": "未付款",
        "paid_status": "已付款",
        "close": "关闭",
        "verify": "验证",
        "enter_pin_to_edit": "输入PIN以编辑",
        "new_prefix": "新",
        "maps_link_label": "地图链接：",
        "add_google_maps": "将您的Google Maps链接添加到发票",
        "google_maps_instructions": "如何获取您的Google Maps链接：",
        "google_maps_step1": "1. 打开Google Maps (google.com/maps)",
        "google_maps_step2": "2. 搜索您的商家名称",
        "google_maps_step3": "3. 点击您的商家",
        "google_maps_step4": "4. 点击'分享'按钮（在照片下方）",
        "google_maps_step5": "5. 点击'复制链接'并粘贴到上方的编辑中",
        "example_link": "链接格式示例：",
        "no_results_for": "未找到",
        "results_count": "个结果",
        "jobs_header": "工作",
        "customers_header": "客户",
        "invoices_header": "发票",
        "id_label": "ID：",
        "optional_fields_hint": "电话、电邮和Google评价是可选的 - 您可以稍后在设置中添加",
        "today": "今天",
        "this_week": "本周",
        "this_month": "本月",
        "owed": "欠款",
        "collected_today": "今日收款",
        "collected_week": "本周收款",
        "collected_month": "本月收款",
        "owed_desc": "待收款",
        "method": "支付方式",
        "mon": "周一", "tue": "周二", "wed": "周三", "thu": "周四", "fri": "周五", "sat": "周六", "sun": "周日",
        "pick_date": "选择日期", "today_btn": "今天", "pick_btn": "选择",
        "show": "显示", "hide": "隐藏",
        "demo_bar": "演示模式 - 剩余{days}天 | 使用许可证密钥激活",
        "waiting_fmt": "等待{count}天",
        "walk_in": "散客", "customer_fallback": "客户",
        "service_label": "服务:", "ready_since": "准备好时间:",
        "due_date_label": "截止日期:", "amount_label": "金额:",
        "please_pickup": "请方便时前来领取。",
        "invoice_label": "发票:", "amount_col": "金额",
        "payment_title": "付款",
        "not_set": "未设置",
        "on_startup": "开启 - 应用将在Windows启动时自动打开",
        "off_startup": "关闭 - 应用将不在Windows启动时自动打开",
        "empty_placeholder": "(空)",
        "format_label": "格式:", "phone_label": "电话:", "email_label": "电邮:",
        "walk_in_customer": "散客",
        "leave_review_label": "请给我们留个Google评价：",
        "google_review_link": "Google评价链接:",
        "no_method": "无付款方式",
        "updated_suffix": "已更新！",
        "maps_link_paste": "粘贴您的Google Maps商家链接：",
        "invalid_google_link": "无效的Google评价链接。\n\n请从Google Maps复制链接：\n1. 在Google Maps搜索您的商家\n2. 点击'分享'或'撰写评价'\n3. 复制链接并粘贴到此处",
        "item_label": "物品", "service_problem": "服务/问题",
        "wa": "WA",
    },
}

def tr(lang, key):
    return T.get(lang, T["en"]).get(key, T["en"].get(key, key))

class App:
    def __init__(self):
        self.db = Database(os.path.join(APP_DIR, "data", "data.db"))
        self.lang = self.db.get_setting("language", "en")
        self.root = tk.Tk()
        self.root.title(tr(self.lang, "app_title"))
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        self.root.configure(bg=C["bg"])
        try:
            self.root.iconbitmap(default="")
        except (tk.TclError, OSError):
            pass
        deleted = self.db.cleanup_old_invoices()
        if deleted > 0:
            self.root.after(100, lambda: messagebox.showinfo(self.t("cleanup"), f"{deleted} {self.t('cleanup_msg')}"))
        deleted_apts = self.db.cleanup_old_appointments()
        if deleted_apts > 0:
            self.root.after(200, lambda: messagebox.showinfo(self.t("cleanup"), f"{deleted_apts} {self.t('cleanup_apts_msg')}"))
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
            return dt.strftime("%d %b %Y")
        except (ValueError, TypeError):
            try:
                dt = datetime.strptime(date_str, "%d/%m/%Y")
                return dt.strftime("%d %b %Y")
            except (ValueError, TypeError):
                return date_str

    def fmt_amount(self, val):
        if val >= 1000000:
            return f"RM {val/1000000:.1f}M"
        if val >= 10000:
            return f"RM {val/1000:.1f}K"
        return f"RM {val:.2f}"

    def truncate(self, text, max_len):
        if not text:
            return ""
        text = str(text)
        if len(text) <= max_len:
            return text
        return text[:max_len-1] + "..."

    def get_review_link(self, google_review):
        if not google_review:
            return ""
        lower = google_review.lower()
        if "write-review" in lower or "/review" in lower.rstrip("/"):
            return google_review
        if "g.page" in lower:
            return google_review.rstrip("/") + "/write-review"
        return google_review

    def tooltip(self, widget, text):
        tip = None
        def on_enter(event):
            nonlocal tip
            if not text or tip is not None:
                return
            tip = tk.Toplevel(widget)
            tip.wm_overrideredirect(True)
            tip.wm_geometry(f"+{event.x_root+12}+{event.y_root+10}")
            lbl = tk.Label(tip, text=text, bg="#222222", fg="#FFFFFF",
                           font=("Segoe UI", 9), padx=8, pady=4, wraplength=400,
                           justify="left")
            lbl.pack()
        def on_leave(event):
            nonlocal tip
            if tip is not None:
                tip.destroy()
                tip = None
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<Button-1>", on_leave)

    def cell(self, parent, text, font=("Segoe UI", 9), bg=C["card"], fg=C["txt"],
             anchor="w", padx=6, tooltip_text=None):
        import tkinter.font as tkfont
        full = str(text)
        lbl = tk.Label(parent, text=full, bg=bg, fg=fg, font=font, anchor=anchor,
                       padx=padx, bd=0)
        fnt = tkfont.Font(root=self.root, font=font)
        last_needed = None
        def fit(event=None):
            nonlocal last_needed
            w = lbl.winfo_width() - padx * 2
            if w <= 0:
                return
            if fnt.measure(full) <= w:
                need = full
            else:
                need = self._fit_to_px(fnt, full, w)
            if need != last_needed:
                lbl.configure(text=need)
                last_needed = need
        lbl.bind("<Configure>", fit)
        self.tooltip(lbl, tooltip_text if tooltip_text is not None else full)
        return lbl

    def _fit_to_px(self, fnt, text, width_px):
        if fnt.measure(text) <= width_px:
            return text
        lo, hi, best = 0, len(text), ""
        while lo <= hi:
            mid = (lo + hi) // 2
            cand = text[:mid]
            if fnt.measure(cand + "...") <= width_px:
                best = cand
                lo = mid + 1
            else:
                hi = mid - 1
        return (best + "...") if best else "..."

    def make_table(self, parent, columns, rows, col_widths):
        header = tk.Frame(parent, bg=C["bg"])
        header.pack(fill="x", pady=(8,2), padx=10)
        for i, (name, width) in enumerate(zip(columns, col_widths)):
            lbl = tk.Label(header, text=name, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 9, "bold"), width=width, anchor="w", padx=4)
            lbl.grid(row=0, column=i, sticky="w", padx=(0,10))
        header.columnconfigure(len(columns)-1, weight=1)
        for row_data in rows:
            r = tk.Frame(parent, bg=C["card"], bd=1, relief="solid", pady=10, padx=10)
            r.pack(fill="x", pady=2, padx=10)
            for i, (text, width, anchor) in enumerate(zip(row_data, col_widths, ["w"]*len(col_widths))):
                if i == len(row_data)-1:
                    anchor = "e"
                lbl = tk.Label(r, text=self.truncate(text, width*2), bg=C["card"], fg=C["txt"], font=("Segoe UI", 9), width=width, anchor=anchor, padx=4)
                lbl.grid(row=0, column=i, sticky="w" if anchor != "e" else "e", padx=(0,10))
            r.columnconfigure(len(row_data)-1, weight=1)
        return header

    def h(self, p):
        return hashlib.sha256(p.encode()).hexdigest()

    def t(self, key):
        return tr(self.lang, key)

    def is_demo(self):
        return is_demo(self.db)

    def check_demo_limit(self):
        if self.is_demo() and len(self.db.get_jobs()) >= 10:
            messagebox.showerror(self.t("error"), self.t("demo_limit"))
            return True
        return False

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

    def get_font_size(self, base_size):
        try:
            width = self.root.winfo_width()
            if width < 1000:
                return max(8, base_size - 2)
            elif width < 1200:
                return max(9, base_size - 1)
            return base_size
        except:
            return base_size

    def search_field(self, parent, placeholder, variable):
        e = tk.Entry(parent, textvariable=variable, font=("Segoe UI", 11), bd=1, relief="solid")
        e.pack(side="left", fill="x", expand=True, ipady=6, padx=(0,10))
        e.insert(0, placeholder)
        e.config(fg=C["txt3"])
        def on_focus_in(event):
            if e.get() == placeholder:
                e.delete(0, tk.END)
                e.config(fg=C["txt"])
        def on_focus_out(event):
            if not e.get():
                e.insert(0, placeholder)
                e.config(fg=C["txt3"])
        def on_keypress(event):
            if e.get() == placeholder:
                e.delete(0, tk.END)
                e.config(fg=C["txt"])
        e.bind("<FocusIn>", on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
        e.bind("<Key>", on_keypress)
        return e

    def btn(self, parent, txt, cmd, bg=None, fg=None):
        b = tk.Button(parent, text=txt, command=cmd, bg=bg or C["pri"], fg=fg or C["white"], font=("Segoe UI", 11, "bold"), bd=0, padx=20, pady=10, cursor="hand2")
        b.bind("<Enter>", lambda e: b.configure(bg=C["pri_h"] if bg == C["pri"] or not bg else bg))
        b.bind("<Leave>", lambda e: b.configure(bg=bg or C["pri"]))
        return b

    def field(self, parent, label, default="", max_len=100):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        e = tk.Entry(f, font=("Segoe UI", 12), bd=1, relief="solid")
        if default:
            e.insert(0, default)
        e.pack(side="left", fill="x", expand=True, ipady=6)
        validate_cmd = (self.root.register(lambda p: len(p) <= max_len), "%P")
        e.configure(validate="key", validatecommand=validate_cmd)
        return e

    def text_area_field(self, parent, label, default="", height=3, max_len=500):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        text = tk.Text(f, font=("Segoe UI", 12), bd=1, relief="solid", height=height, wrap="word")
        text.pack(side="left", fill="x", expand=True, ipady=4)
        if default:
            text.insert("1.0", default)
        _orig_get = text.get
        def get_text():
            return _orig_get("1.0", "end-1c")
        def on_key_release(event=None):
            content = get_text()
            filtered = content.replace("<", "").replace(">", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("|", "").replace("\\", "")
            if filtered != content:
                pos = text.index("insert")
                text.delete("1.0", "end-1c")
                text.insert("1.0", filtered)
                text.mark_set("insert", pos)
            if len(get_text()) > max_len:
                text.delete("1.0", f"1.{max_len}")
        text.bind("<KeyRelease>", on_key_release)
        text.get = get_text
        return text

    def phone_field(self, parent, label, default="+60"):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        e = tk.Entry(f, textvariable=var, font=("Segoe UI", 12), bd=1, relief="solid")
        e.pack(side="left", fill="x", expand=True, ipady=6)
        validate_cmd = (self.root.register(lambda p: all(c.isdigit() or c in "+- " for c in p) and len(p) <= 20), "%P")
        e.configure(validate="key", validatecommand=validate_cmd)
        return e

    def email_field(self, parent, label, default=""):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        e = tk.Entry(f, font=("Segoe UI", 12), bd=1, relief="solid")
        if default:
            e.insert(0, default)
        e.pack(side="left", fill="x", expand=True, ipady=6)
        def validate_email(p):
            if not p:
                return True
            if len(p) > 80:
                return False
            if any(c in p for c in "<>(){}[]|\\"):
                return False
            return True
        validate_cmd = (self.root.register(validate_email), "%P")
        e.configure(validate="key", validatecommand=validate_cmd)
        return e

    def number_field(self, parent, label, default=""):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        e = tk.Entry(f, textvariable=var, font=("Segoe UI", 12), bd=1, relief="solid")
        e.pack(side="left", fill="x", expand=True, ipady=6)
        validate_cmd = (self.root.register(lambda p: (all(c.isdigit() or c in ".-" for c in p) and len(p) <= 12)), "%P")
        e.configure(validate="key", validatecommand=validate_cmd)
        return e

    def name_field(self, parent, label, default=""):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        e = tk.Entry(f, textvariable=var, font=("Segoe UI", 12), bd=1, relief="solid")
        e.pack(side="left", fill="x", expand=True, ipady=6)
        def validate_name(p):
            if not p:
                return True
            if len(p) > 50:
                return False
            if any(c in p for c in "<>(){}[]|\\\"'"):
                return False
            return True
        validate_cmd = (self.root.register(validate_name), "%P")
        e.configure(validate="key", validatecommand=validate_cmd)
        return e

    def pin_field(self, parent, label, default=""):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        e = tk.Entry(f, textvariable=var, font=("Segoe UI", 12), bd=1, relief="solid", show="*")
        e.pack(side="left", fill="x", expand=True, ipady=6)
        validate_cmd = (self.root.register(lambda p: all(c.isdigit() for c in p) and len(p) <= 4), "%P")
        e.configure(validate="key", validatecommand=validate_cmd)
        def toggle_show():
            if e.cget("show") == "*":
                e.configure(show="")
                show_btn.configure(text=self.t("hide"))
            else:
                e.configure(show="*")
                show_btn.configure(text=self.t("show"))
        show_btn = tk.Button(f, text=self.t("show"), command=toggle_show, bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), bd=1, relief="solid", padx=6, cursor="hand2")
        show_btn.pack(side="left", padx=4)
        return e

    def date_field(self, parent, label, default=None):
        import calendar
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        today = datetime.now() if not default else datetime.strptime(default, "%Y-%m-%d")
        frame = tk.Frame(f, bg=C["bg"])
        frame.pack(side="left")
        year_var = tk.StringVar(value=str(today.year))
        month_var = tk.StringVar(value=f"{today.month:02d}")
        day_var = tk.StringVar(value=f"{today.day:02d}")
        def validate_digits(p):
            if p == "" or p.isdigit():
                return True
            return False
        vcmd = (self.root.register(validate_digits), "%P")
        year_e = tk.Spinbox(frame, from_=2020, to=2099, textvariable=year_var, width=6, font=("Segoe UI", 12), bd=1, relief="solid", justify="center", validate="key", validatecommand=vcmd)
        year_e.pack(side="left")
        tk.Label(frame, text="-", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(side="left")
        month_e = tk.Spinbox(frame, from_=1, to=12, textvariable=month_var, width=3, font=("Segoe UI", 12), bd=1, relief="solid", justify="center", format="%02.0f", validate="key", validatecommand=vcmd)
        month_e.pack(side="left")
        tk.Label(frame, text="-", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(side="left")
        def get_days(*args):
            try:
                y = int(year_var.get())
                m = int(month_var.get())
                return calendar.monthrange(y, m)[1]
            except:
                return 31
        day_e = tk.Spinbox(frame, from_=1, to=get_days(), textvariable=day_var, width=3, font=("Segoe UI", 12), bd=1, relief="solid", justify="center", format="%02.0f", validate="key", validatecommand=vcmd)
        day_e.pack(side="left")
        def update_days(*args):
            day_e.configure(to=get_days())
        year_var.trace_add("write", update_days)
        month_var.trace_add("write", update_days)
        class DateStr:
            def __init__(self, yv, mv, dv):
                self.yv = yv
                self.mv = mv
                self.dv = dv
            def get(self):
                return f"{self.yv.get()}-{self.mv.get()}-{self.dv.get()}"
            def set(self, val):
                try:
                    parts = val.split("-")
                    self.yv.set(parts[0])
                    self.mv.set(f"{int(parts[1]):02d}")
                    self.dv.set(f"{int(parts[2]):02d}")
                except:
                    pass
        var = DateStr(year_var, month_var, day_var)
        def show_cal():
            win = tk.Toplevel(self.root)
            win.title(self.t("pick_date"))
            win.geometry("280x320")
            win.configure(bg=C["bg"])
            win.grab_set()
            try:
                current = datetime.strptime(var.get(), "%Y-%m-%d")
            except (ValueError, TypeError):
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
                for d in [self.t("mon"), self.t("tue"), self.t("wed"), self.t("thu"), self.t("fri"), self.t("sat"), self.t("sun")]:
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
                tk.Button(cal_frame, text=self.t("today_btn"), command=lambda: [var.set(datetime.now().strftime("%Y-%m-%d")), win.destroy()], bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10), bd=1, relief="solid", padx=15, pady=5, cursor="hand2").pack(pady=10)
            cal_frame = tk.Frame(win, bg=C["bg"])
            cal_frame.pack(fill="both", expand=True, padx=10, pady=10)
            draw_calendar()
        tk.Button(frame, text=self.t("pick_btn"), command=show_cal, bg=C["card"], fg=C["txt"], font=("Segoe UI", 10), bd=1, relief="solid", padx=8, cursor="hand2").pack(side="left", padx=5)
        return var

    def time_field(self, parent, label, default=None):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", pady=8)
        tk.Label(f, text=label, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
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
        tk.Label(c, text=self.t("optional_fields_hint"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack(pady=(0,8))
        f = tk.Frame(c, bg=C["bg"]); f.pack()
        self.se = {}
        self.se["Business Name"] = self.field(f, self.t("business_name"), "")
        self.se["Phone"] = self.phone_field(f, self.t("phone"), "+60")
        self.se["Email"] = self.email_field(f, self.t("email"), "")
        gf = tk.Frame(f, bg=C["bg"]); gf.pack(fill="x", pady=8)
        tk.Label(gf, text=self.t("google_review"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        self.se["Google Review"] = tk.Entry(gf, font=("Segoe UI", 12), bd=1, relief="solid")
        self.se["Google Review"].pack(side="left", fill="x", expand=True, ipady=6)
        def validate_review(p):
            if not p:
                return True
            if any(c in p for c in "<>(){}[]|\\"):
                return False
            return True
        review_validate = (self.root.register(validate_review), "%P")
        self.se["Google Review"].configure(validate="key", validatecommand=review_validate)
        tk.Label(gf, text=self.t("google_review_hint"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 9)).pack(side="left", padx=8)
        lf = tk.Frame(f, bg=C["bg"]); lf.pack(fill="x", pady=12)
        tk.Label(lf, text=self.t("language"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        self.lang_var = tk.StringVar(value="en")
        for v, t in [("en","English"),("ms","Bahasa Malaysia"),("zh","Chinese")]:
            tk.Radiobutton(lf, text=t, variable=self.lang_var, value=v, bg=C["bg"], font=("Segoe UI", 11)).pack(side="left", padx=8)
        self.btn(c, self.t("get_started"), self.save_wizard).pack(pady=30)
        tk.Label(c, text=self.t("offline_msg"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack()

    def save_wizard(self):
        n = self.se["Business Name"].get().strip()
        if not n:
            return messagebox.showerror(self.t("error"), self.t("enter_business_name"))
        self.db.set_setting("business_name", n)
        self.db.set_setting("business_phone", self.se["Phone"].get().strip())
        self.db.set_setting("business_email", self.se["Email"].get().strip())
        self.db.set_setting("google_review", self.se["Google Review"].get().strip())
        self.db.set_setting("language", self.lang_var.get())
        self.db.set_setting("setup_complete", "true")
        self.layout()

    def pin_screen(self):
        self.clr()
        self.root.configure(bg=C["bg"])
        c = tk.Frame(self.root, bg=C["bg"]); c.pack(expand=True, fill="both")
        n = self.db.get_setting("business_name", "Shop")
        tk.Label(c, text=n, bg=C["bg"], fg=C["txt"], font=("Segoe UI", 26, "bold")).pack(pady=8)
        tk.Label(c, text=self.t("enter_pin"), bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 12)).pack(pady=8)
        pf = tk.Frame(c, bg=C["bg"])
        pf.pack(pady=8)
        self.pin_e = tk.Entry(pf, font=("Segoe UI", 24), bd=1, relief="solid", width=8, justify="center", show="*")
        self.pin_e.pack(side="left", ipady=8)
        def toggle_pin():
            if self.pin_e.cget("show") == "*":
                self.pin_e.configure(show="")
                pin_btn.configure(text=self.t("hide"))
            else:
                self.pin_e.configure(show="*")
                pin_btn.configure(text=self.t("show"))
        pin_btn = tk.Button(pf, text=self.t("show"), command=toggle_pin, bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10), bd=1, relief="solid", padx=8, cursor="hand2")
        pin_btn.pack(side="left", padx=8)
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
        tk.Label(c, text=self.t("license_activation"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 24, "bold")).pack(pady=8)
        tk.Label(c, text=self.t("enter_license_key"), bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 12)).pack(pady=5)
        hwid_frame = tk.Frame(c, bg=C["card"], bd=1, relief="solid", padx=15, pady=10)
        hwid_frame.pack(pady=15, padx=40, fill="x")
        tk.Label(hwid_frame, text=self.t("your_hwid"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w")
        hwid_row = tk.Frame(hwid_frame, bg=C["card"])
        hwid_row.pack(fill="x", pady=5)
        tk.Label(hwid_row, text=hwid, bg=C["card"], fg=C["pri"], font=("Consolas", 16, "bold")).pack(side="left")
        def copy_hwid():
            self.root.clipboard_clear()
            self.root.clipboard_append(hwid)
            messagebox.showinfo(self.t("done"), self.t("hwid_copied"))
        copy_btn = tk.Button(hwid_row, text=self.t("copy"), command=copy_hwid, bg=C["pri"], fg=C["white"], font=("Segoe UI", 10, "bold"), bd=0, padx=12, pady=4, cursor="hand2")
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
                messagebox.showinfo(self.t("done"), self.t("activated"))
                if not self.db.get_setting("setup_complete"):
                    self.wizard()
                else:
                    self.layout()
            else:
                messagebox.showerror(self.t("error"), self.t("invalid_key"))
        def try_demo():
            if not is_demo(self.db):
                messagebox.showerror(self.t("error"), self.t("demo_expired"))
                return
            for w in self.root.winfo_children():
                w.destroy()
            if not self.db.get_setting("setup_complete"):
                self.wizard()
            else:
                self.layout()
        b = tk.Button(bf, text=self.t("activate"), command=activate, bg=C["pri"], fg=C["white"], font=("Segoe UI", 12, "bold"), bd=0, padx=30, pady=10, cursor="hand2")
        b.pack(side="left", padx=5)
        b.bind("<Enter>", lambda e: b.configure(bg=C["pri_h"]))
        b.bind("<Leave>", lambda e: b.configure(bg=C["pri"]))
        b2 = tk.Button(bf, text=self.t("try_demo"), command=try_demo, bg=C["card"], fg=C["txt"], font=("Segoe UI", 12), bd=1, relief="solid", padx=20, pady=10, cursor="hand2")
        b2.pack(side="left", padx=5)
        tk.Label(c, text=self.t("demo_mode"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack(pady=10)
        tk.Label(c, text=self.t("contact_seller"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack()

    def layout(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=C["bg"])
        self.root.title(self.t("app_title"))
        self.side = tk.Frame(self.root, bg=C["side"], width=200)
        self.side.pack(side="left", fill="y")
        self.side.pack_propagate(False)
        main_frame = tk.Frame(self.root, bg=C["bg"])
        main_frame.pack(side="left", fill="both", expand=True)
        if self.is_demo():
            days_left = 7
            try:
                install_date = self.db.get_setting("install_date")
                if install_date:
                    days_left = 7 - (datetime.now() - datetime.fromisoformat(install_date)).days
            except (ValueError, TypeError):
                pass
            demo_bar = tk.Frame(main_frame, bg="#FEF3C7", height=30)
            demo_bar.pack(fill="x", side="top")
            demo_bar.pack_propagate(False)
            tk.Label(demo_bar, text=self.t("demo_bar").format(days=days_left), bg="#FEF3C7", fg="#92400E", font=("Segoe UI", 10, "bold")).pack(expand=True)
        self.content_canvas = tk.Canvas(main_frame, bg=C["bg"], highlightthickness=0, bd=0)
        self.content_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.content_canvas.yview)
        self.content = tk.Frame(self.content_canvas, bg=C["bg"])
        self.content.bind("<Configure>", lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))
        self.canvas_window = self.content_canvas.create_window((0, 0), window=self.content, anchor="nw", tags="inner")
        self.content_canvas.configure(yscrollcommand=self.content_scrollbar.set)
        self.content_scrollbar.pack(side="right", fill="y")
        self.content_canvas.pack(side="left", fill="both", expand=True)
        def on_canvas_configure(event):
            self.content_canvas.itemconfig("inner", width=event.width)
            self.content.configure(width=event.width)
        self.content_canvas.bind("<Configure>", on_canvas_configure)
        def _on_mousewheel(event):
            current = self.content_canvas.yview()
            if event.delta > 0 and current[0] <= 0:
                return
            self.content_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        def _bind_mousewheel(event):
            self.content_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_mousewheel(event):
            self.content_canvas.unbind_all("<MouseWheel>")
        self.content_canvas.bind("<Enter>", _bind_mousewheel)
        self.content_canvas.bind("<Leave>", _unbind_mousewheel)
        n = self.db.get_setting("business_name", "Shop")
        name_label = tk.Label(self.side, text=n, bg=C["side"], fg=C["white"], font=("Segoe UI", 13, "bold"), pady=15, wraplength=170, justify="center")
        name_label.pack(fill="x", padx=10)
        tk.Frame(self.side, bg="#2A2A2A", height=1).pack(fill="x", padx=15)
        for txt, cmd in [("Home", self.pg_home), ("Jobs", self.pg_jobs), ("Customers", self.pg_custs),
                         ("Appointments", self.pg_cal), ("Invoices", self.pg_invs), ("Reports", self.pg_rpt),
                         ("Backup", self.pg_backup), ("Settings", self.pg_set)]:
            b = tk.Button(self.side, text=f"  {self.t(txt.lower())}", command=cmd, bg=C["side"], fg="#AAAAAA", font=("Segoe UI", 11), bd=0, anchor="w", padx=20, pady=12, activebackground=C["side_h"], activeforeground=C["white"], cursor="hand2")
            b.pack(fill="x")
            b.bind("<Enter>", lambda e, b=b: b.configure(bg=C["side_h"], fg=C["white"]))
            b.bind("<Leave>", lambda e, b=b: b.configure(bg=C["side"], fg="#AAAAAA"))
        self.root.after(10, self.pg_home)

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
        done_count = len([j for j in jobs if j["status"] == "done" and (j["completed_at"] or "").startswith(datetime.now().strftime("%Y-%m"))])
        for i, (l, v, cmd) in enumerate([(self.t("active_jobs"), str(active), self.pg_jobs), (self.t("appointments"), str(appts), self.pg_cal), (self.t("outstanding"), self.fmt_amount(owed), self.pg_invs), (self.t("jobs_done"), str(done_count), self.pg_jobs)]):
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
                rems.append(f"{j['job_code']}: {j['item']} - {self.t('ready')}")
        for a in self.db.get_appointments(today):
            rems.append(f"{a['time']} - {a['customer_name'] or self.t('walk_in')}")
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
            tk.Label(uf, text=f"{self.t('waiting_for_pickup_count')} ({len(uncollected)})", bg=C["bg"], fg=C["warn"], font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=8)
            for j in uncollected[:5]:
                row = tk.Frame(uf, bg="#FEF3C7", bd=1, relief="solid", pady=8, padx=14)
                row.pack(fill="x", pady=3)
                left = tk.Frame(row, bg="#FEF3C7")
                left.pack(side="left", fill="x", expand=True)
                tk.Label(left, text=f"{j['customer_name'] or self.t('unknown')} - {j['item']}", bg="#FEF3C7", fg="#92400E", font=("Segoe UI", 11), anchor="w").pack(fill="x")
                tk.Label(left, text=self.t("waiting_fmt").format(count=j["days_waiting"]), bg="#FEF3C7", fg="#92400E", font=("Segoe UI", 10)).pack(fill="x")
                def send_pickup_reminder(job=j):
                    phone = (job["customer_phone"] or "").replace("+","").replace("-","").replace(" ","")
                    if not phone:
                        return messagebox.showwarning(self.t("no_phone_short"), self.t("no_phone"))
                    if not phone.startswith("60"):
                        phone = "60" + phone
                    biz_name = self.db.get_setting("business_name", "Shop")
                    msg = f"Hi {job['customer_name'] or self.t('customer_fallback')},\n\n"
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
                    except (webbrowser.Error, OSError):
                        pass
                    messagebox.showinfo(self.t("done"), self.t("whatsapp_opened") + f" +{phone}")
                tk.Button(row, text=self.t("send_reminder"), command=send_pickup_reminder, bg=C["warn"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=8, pady=2, cursor="hand2").pack(side="right")
        self.root.after(50, lambda: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))

    def pg_jobs(self):
        self.clr()
        self.hdr(self.t("jobs"), self.t("new_job"), self.pg_new_job)
        f = tk.Frame(self.content, bg=C["bg"], padx=12)
        f.pack(fill="both", expand=True)
        sf = tk.Frame(f, bg=C["bg"])
        sf.pack(fill="x", pady=(0, 10))
        self.jobs_search_var = tk.StringVar()
        self.search_field(sf, self.t("search_jobs"), self.jobs_search_var)
        self.jobs_list_frame = tk.Frame(f, bg=C["bg"])
        self.jobs_list_frame.pack(fill="both", expand=True)
        self.jobs_search_var.trace("w", lambda *a: self._filter_jobs())
        self._filter_jobs()
        self.root.after(50, lambda: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))

    def _filter_jobs(self):
        for w in self.jobs_list_frame.winfo_children():
            w.destroy()
        jobs = self.db.get_jobs()
        q = self.jobs_search_var.get().strip().lower()
        if q and q != self.t("search_jobs").lower():
            jobs = [j for j in jobs if q in (j["job_code"]+j["item"]+(j["problem"] or "")+(j["customer_name"] or "")+(j["notes"] or "")).lower()]
        if not jobs:
            tk.Label(self.jobs_list_frame, text=self.t("no_jobs") if not q else self.t("no_results"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
            return
        table = tk.Frame(self.jobs_list_frame, bg=C["bg"])
        table.pack(fill="both", expand=True, padx=8)
        col_names = [self.t("code"), self.t("customer"), self.t("item"), self.t("quote"), self.t("status"), self.t("due_date"), self.t("notes"), "", self.t("action")]
        col_wt = [2, 2, 3, 1, 1, 1, 2, 0, 0]
        col_minsize = [110, 100, 150, 75, 75, 105, 90, 60, 50]
        for i in range(9):
            table.grid_columnconfigure(i, weight=col_wt[i], minsize=col_minsize[i])
        for i, name in enumerate(col_names):
            if name:
                tk.Label(table, text=name, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10, "bold"), anchor="w", padx=4).grid(row=0, column=i, sticky="w", pady=(8, 4))
        sc = {"pending": C["warn"], "in-progress": "#2563EB", "done": C["ok"]}
        for ri, j in enumerate(jobs):
            row_bg = C["card"] if ri % 2 == 0 else C["bg"]
            row = ri + 1
            table.rowconfigure(row, pad=12)
            self.cell(table, j["job_code"], font=("Segoe UI", 11, "bold"), bg=row_bg, fg=C["txt"], tooltip_text=j["job_code"]).grid(row=row, column=0, sticky="ew", padx=2)
            self.cell(table, j["customer_name"] or "-", font=("Segoe UI", 11), bg=row_bg, fg=C["txt2"], tooltip_text=j["customer_name"] or "").grid(row=row, column=1, sticky="ew", padx=2)
            self.cell(table, j["item"], font=("Segoe UI", 11), bg=row_bg, fg=C["txt"], tooltip_text=j["item"]).grid(row=row, column=2, sticky="ew", padx=2)
            self.cell(table, self.fmt_amount(float(j['quote'] or 0)), font=("Segoe UI", 11, "bold"), bg=row_bg, fg=C["txt"]).grid(row=row, column=3, sticky="ew", padx=2)
            tk.Label(table, text=self.t(j["status"].replace("-","_")), bg=sc.get(j["status"], "#999"), fg=C["white"], font=("Segoe UI", 10, "bold"), anchor="center", padx=4).grid(row=row, column=4, sticky="ew", padx=2)
            self.cell(table, self.fmt_date(j["due_date"]), font=("Segoe UI", 11), bg=row_bg, fg=C["txt2"]).grid(row=row, column=5, sticky="ew", padx=2)
            self.cell(table, j["notes"] or "-", font=("Segoe UI", 11), bg=row_bg, fg=C["txt2"], tooltip_text=j["notes"] or "").grid(row=row, column=6, sticky="ew", padx=2)
            if j["status"] != "done":
                tk.Button(table, text=self.t("done"), command=lambda j=j: self.mark_done(j), bg=C["ok"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, cursor="hand2").grid(row=row, column=7, sticky="e", padx=1)
            if j["status"] == "done":
                invs = self.db.get_invoices()
                has_inv = any(i["job_id"] == j["id"] for i in invs)
                if not has_inv:
                    tk.Button(table, text=self.t("pdf"), command=lambda j=j: self.download_job_pdf(j), bg="#2563EB", fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, cursor="hand2").grid(row=row, column=7, sticky="e", padx=1)
            tk.Button(table, text=self.t("edit"), command=lambda j=j: self.edit_job(j), bg=row_bg, fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, cursor="hand2").grid(row=row, column=8, sticky="e", padx=1)

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
            inv = invs[-1] if invs else None
        if not inv:
            return messagebox.showerror(self.t("error"), self.t("pdf_failed"))
        cust = self.db.get_customer(job["customer_id"]) if job["customer_id"] else None
        pdf_path = self.generate_invoice_pdf(inv["invoice_code"], job, cust)
        if pdf_path:
            messagebox.showinfo(self.t("done"), self.t("pdf_saved") + f"\n{pdf_path}")
            try:
                os.startfile(os.path.dirname(pdf_path))
            except (OSError, AttributeError):
                pass

    def pg_new_job(self):
        self.clr()
        self.hdr(self.t("new_job_title"))
        f = tk.Frame(self.content, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        self.je = {}
        cf = tk.Frame(f, bg=C["bg"])
        cf.pack(fill="x", pady=8)
        tk.Label(cf, text=self.t("customer"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        customers = self.db.get_customers()
        cust_names = [c["name"] for c in customers] if customers else []
        self.cust_map = {c["name"]: c for c in customers} if customers else {}
        self.je["Customer"] = tk.StringVar()
        self.cust_entry = tk.Entry(cf, font=("Segoe UI", 12), bd=1, relief="solid")
        self.cust_entry.pack(side="left", fill="x", expand=True, ipady=6)
        def validate_cust(p):
            if not p:
                return True
            if any(c in p for c in "<>(){}[]|\\\"'"):
                return False
            return True
        cust_validate = (self.root.register(validate_cust), "%P")
        self.cust_entry.configure(validate="key", validatecommand=cust_validate)
        if cust_names:
            tk.Label(cf, text=self.t("or_pick"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10)).pack(side="left", padx=(10,5))
            self.cust_menu_var = tk.StringVar()
            menu = tk.OptionMenu(cf, self.cust_menu_var, *cust_names, command=self._pick_cust)
            menu.configure(font=("Segoe UI", 10), width=15)
            menu.pack(side="left", ipady=4)
        pf = tk.Frame(f, bg=C["bg"])
        pf.pack(fill="x", pady=8)
        tk.Label(pf, text=self.t("phone"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        self.je["Phone"] = tk.Entry(pf, font=("Segoe UI", 12), bd=1, relief="solid")
        self.je["Phone"].insert(0, "+60")
        self.je["Phone"].pack(side="left", fill="x", expand=True, ipady=6)
        phone_validate = (self.root.register(lambda p: all(c.isdigit() or c in "+- " for c in p) and len(p) <= 20), "%P")
        self.je["Phone"].configure(validate="key", validatecommand=phone_validate)
        ef = tk.Frame(f, bg=C["bg"])
        ef.pack(fill="x", pady=8)
        tk.Label(ef, text=self.t("email"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        self.je["Email"] = tk.Entry(ef, font=("Segoe UI", 12), bd=1, relief="solid")
        self.je["Email"].pack(side="left", fill="x", expand=True, ipady=6)
        email_validate = (self.root.register(lambda p: all(c not in "<>(){}[]|\\" for c in p) and len(p) <= 80), "%P")
        self.je["Email"].configure(validate="key", validatecommand=email_validate)
        for l in ["Item", "Problem"]:
            self.je[l] = self.field(f, self.t(l.lower()))
        self.je["Notes"] = self.text_area_field(f, self.t("notes"))
        self.je["Quote (RM)"] = self.number_field(f, self.t("quote"))
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
        if not cust_name:
            return messagebox.showerror(self.t("error"), self.t("enter_name"))
        phone = self.je["Phone"].get().strip()
        email = self.je["Email"].get().strip()
        item = self.je["Item"].get().strip()
        if not item:
            return messagebox.showerror(self.t("error"), self.t("enter_item"))
        try:
            q = float(self.je["Quote (RM)"].get().strip() or "0")
        except ValueError:
            return messagebox.showerror(self.t("error"), self.t("quote_number"))
        if self.check_demo_limit():
            return
        cid = None
        if cust_name:
            if cust_name in self.cust_map:
                cid = self.cust_map[cust_name]["id"]
            else:
                cid = self.db.add_customer(cust_name, phone, email)
        due = self.je["Due Date"].get() if isinstance(self.je["Due Date"], tk.StringVar) else self.je["Due Date"].get().strip()
        self.db.add_job(cid, item, self.je["Problem"].get().strip(), q, due, self.je["Notes"].get().strip())
        messagebox.showinfo(self.t("done"), self.t("job_saved"))
        self.pg_jobs()

    def edit_job(self, j):
        win = tk.Toplevel(self.root)
        win.title(self.t("edit_job_title"))
        win.geometry("620x580")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text=self.t("edit_job_title"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 16, "bold")).pack(pady=10)
        f = tk.Frame(win, bg=C["bg"], padx=30)
        f.pack(fill="both", expand=True)
        item_e = self.field(f, self.t("item"), j["item"])
        problem_e = self.field(f, self.t("problem"), j["problem"] or "")
        quote_e = self.number_field(f, self.t("quote"), str(j["quote"]))
        status_frame = tk.Frame(f, bg=C["bg"])
        status_frame.pack(fill="x", pady=8)
        tk.Label(status_frame, text=self.t("status"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        status_var = tk.StringVar(value=j["status"])
        for v, lbl in [("pending",self.t("pending")),("in-progress",self.t("in_progress")),("done",self.t("done"))]:
            tk.Radiobutton(status_frame, text=lbl, variable=status_var, value=v, bg=C["bg"], font=("Segoe UI", 11)).pack(side="left", padx=8)
        due_var = self.date_field(f, self.t("due_date"), j["due_date"])
        notes_e = self.text_area_field(f, self.t("notes"), j["notes"] or "")
        bf = tk.Frame(f, bg=C["bg"], pady=15)
        bf.pack(fill="x")
        def save():
            try:
                q = float(quote_e.get().strip() or "0")
            except ValueError:
                return messagebox.showerror(self.t("error"), self.t("quote_number"))
            due = due_var.get() if isinstance(due_var, tk.StringVar) else due_var.get().strip()
            self.db.update_job(j["id"], item_e.get().strip(), problem_e.get().strip(), q, status_var.get(), due, notes_e.get().strip())
            win.destroy()
            messagebox.showinfo(self.t("done"), self.t("job_updated"))
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
        win.title(self.t("job_complete_title"))
        win.geometry("360x400")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text=self.t("job_complete_title"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 16, "bold")).pack(pady=8)
        tk.Label(win, text=job["item"], bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 12)).pack()
        tk.Label(win, text=self.fmt_amount(job['quote']), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 14, "bold")).pack(pady=5)
        cust = self.db.get_customer(job["customer_id"]) if job["customer_id"] else None
        has_inv = self._job_has_invoice(job["id"])
        if has_inv:
            tk.Label(win, text=self.t("invoice_already_exists"), bg=C["bg"], fg=C["warn"], font=("Segoe UI", 9)).pack()
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
                if use_pdf and pdf_path:
                    msg = f"Hi {cust['name'] if cust else 'Customer'},\n\n"
                    msg += f"Your {job['item']} service is ready for collection!\n\n"
                    msg += f"Invoice: {inv_code}\n"
                    msg += f"Amount: {self.fmt_amount(job['quote'])}\n"
                    msg += f"Please find the attached PDF invoice.\n"
                    thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
                    msg += f"\n{thank_you}\n{self.db.get_setting('business_name', 'Shop')}"
                    try:
                        subprocess.run(["explorer", "/select,", pdf_path], check=False)
                    except (OSError, FileNotFoundError):
                        try:
                            os.startfile(os.path.dirname(pdf_path))
                        except (OSError, AttributeError):
                            pass
                else:
                    msg = f"Hi {cust['name'] if cust else 'Customer'},\n\n"
                    msg += f"Your {job['item']} service is ready for collection!\n\n"
                    if job['problem']:
                        msg += f"Service: {job['problem']}\n"
                    msg += f"Ready since: {self.fmt_date(datetime.now().strftime('%Y-%m-%d'))}\n\n"
                    if job["due_date"]:
                        msg += f"Due Date: {self.fmt_date(job['due_date'])}\n"
                    payment_terms = self.db.get_setting("payment_terms", "")
                    if payment_terms:
                        msg += f"{payment_terms}\n"
                    msg += f"Please pick up at your convenience.\n\n"
                    msg += f"Invoice: {inv_code}\n"
                    msg += f"Amount: {self.fmt_amount(job['quote'])}\n\n"
                    google_review = self.db.get_setting("google_review", "")
                    if google_review:
                        review_link = self.get_review_link(google_review)
                        if review_link:
                            msg += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
                    thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
                    msg += f"{thank_you}\n{self.db.get_setting('business_name', 'Shop')}"
                url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                try:
                    webbrowser.open(url)
                except (webbrowser.Error, OSError):
                    pass
                if use_pdf and pdf_path:
                    messagebox.showinfo(self.t("done"), self.t("invoice_created") + f"\n{self.t('opening_whatsapp')} +{phone}\n{self.t('pdf_opened')}")
                else:
                    messagebox.showinfo(self.t("done"), self.t("invoice_created") + f"\n{self.t('opening_whatsapp')} +{phone}")
            else:
                messagebox.showwarning(self.t("warning"), self.t("invoice_created") + "\n" + self.t("no_phone"))
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
                    if job["due_date"]:
                        body += f"Due Date: {self.fmt_date(job['due_date'])}\n"
                    payment_terms = self.db.get_setting("payment_terms", "")
                    if payment_terms:
                        body += f"{payment_terms}\n"
                    body += f"Amount: {self.fmt_amount(job['quote'])}\n\n"
                    google_review = self.db.get_setting("google_review", "")
                    if google_review:
                        review_link = self.get_review_link(google_review)
                        if review_link:
                            body += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
                    thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
                    body += f"{thank_you}\n{biz_name}"
                    mailto = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
                    try:
                        webbrowser.open(mailto)
                        os.startfile(pdf_path)
                    except (webbrowser.Error, OSError):
                        pass
                    messagebox.showinfo(self.t("done"), self.t("invoice_created") + f"\n{self.t('email_opened')} {email}\n{self.t('pdf_saved')} {pdf_path}")
                else:
                    body = f"Dear {cust['name'] if cust else 'Customer'},\n\n"
                    thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
                    body += f"{thank_you}\n\n"
                    body += f"Invoice: {inv_code}\nDate: {self.fmt_date(datetime.now().strftime('%Y-%m-%d'))}\nItem: {job['item']}\nService: {job['problem'] or 'N/A'}\nAmount: {self.fmt_amount(job['quote'])}\n\n"
                    if job["due_date"]:
                        body += f"Due Date: {self.fmt_date(job['due_date'])}\n"
                    payment_terms = self.db.get_setting("payment_terms", "")
                    if payment_terms:
                        body += f"{payment_terms}\n"
                    google_review = self.db.get_setting("google_review", "")
                    if google_review:
                        review_link = self.get_review_link(google_review)
                        if review_link:
                            body += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
                    body += f"{thank_you}\n{biz_name}"
                    mailto = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
                    try:
                        webbrowser.open(mailto)
                    except (webbrowser.Error, OSError):
                        pass
                    messagebox.showinfo(self.t("done"), self.t("invoice_created") + f"\n{self.t('email_opened')} {email}")
            else:
                messagebox.showwarning(self.t("warning"), self.t("invoice_created") + "\n" + self.t("no_email"))
            self.pg_jobs()
        def just_inv():
            self._get_or_create_invoice(job)
            win.destroy()
            messagebox.showinfo(self.t("done"), self.t("invoice_created"))
            self.pg_jobs()
        self.btn(win, self.t("invoice_whatsapp"), send_inv).pack(fill="x", padx=25, pady=5)
        self.btn(win, self.t("invoice_email"), send_email_inv, bg="#2563EB").pack(fill="x", padx=25, pady=5)
        self.btn(win, self.t("just_invoice"), just_inv, bg=C["card"], fg=C["txt"]).pack(fill="x", padx=25, pady=5)
        tk.Button(win, text=self.t("skip"), command=win.destroy, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10), bd=0, cursor="hand2").pack(pady=10)

    def pg_custs(self):
        self.clr()
        self.hdr(self.t("customers"), self.t("new_customer"), self.pg_new_cust)
        f = tk.Frame(self.content, bg=C["bg"], padx=12)
        f.pack(fill="both", expand=True)
        sf = tk.Frame(f, bg=C["bg"])
        sf.pack(fill="x", pady=(0,10))
        self.cust_search_var = tk.StringVar()
        self.search_field(sf, self.t("search_customers"), self.cust_search_var)
        self.cust_list_frame = tk.Frame(f, bg=C["bg"])
        self.cust_list_frame.pack(fill="both", expand=True)
        self.cust_search_var.trace("w", lambda *a: self._filter_custs())
        self._filter_custs()
        self.root.after(50, lambda: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))

    def _filter_custs(self):
        for w in self.cust_list_frame.winfo_children():
            w.destroy()
        cs = self.db.get_customers()
        q = self.cust_search_var.get().strip().lower()
        if q and q != self.t("search_customers").lower():
            cs = [c for c in cs if q in (c["name"]+(c["phone"] or "")+(c["email"] or "")).lower()]
        if not cs:
            tk.Label(self.cust_list_frame, text=self.t("no_customers") if not q else self.t("no_results"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
            return
        table = tk.Frame(self.cust_list_frame, bg=C["bg"])
        table.pack(fill="both", expand=True, padx=8)
        col_names = [self.t("name"), self.t("phone"), self.t("email"), ""]
        col_wt = [3, 2, 3, 0]
        col_minsize = [180, 130, 180, 80]
        for i in range(4):
            table.grid_columnconfigure(i, weight=col_wt[i], minsize=col_minsize[i])
        for i, name in enumerate(col_names):
            if name:
                tk.Label(table, text=name, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10, "bold"), anchor="w", padx=4).grid(row=0, column=i, sticky="w", pady=(8, 4))
        for ri, c in enumerate(cs):
            row_bg = C["card"] if ri % 2 == 0 else C["bg"]
            row = ri + 1
            table.rowconfigure(row, pad=12)
            self.cell(table, c["name"], font=("Segoe UI", 11, "bold"), bg=row_bg, fg=C["txt"], tooltip_text=c["name"]).grid(row=row, column=0, sticky="ew", padx=2)
            self.cell(table, c["phone"] or "-", font=("Segoe UI", 11), bg=row_bg, fg=C["txt2"]).grid(row=row, column=1, sticky="ew", padx=2)
            self.cell(table, c["email"] or "-", font=("Segoe UI", 11), bg=row_bg, fg=C["txt2"], tooltip_text=c["email"] or "").grid(row=row, column=2, sticky="ew", padx=2)
            tk.Button(table, text=self.t("edit"), command=lambda c=c: self.edit_cust(c), bg=row_bg, fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, cursor="hand2").grid(row=row, column=3, sticky="e", padx=1)

    def edit_cust(self, c):
        win = tk.Toplevel(self.root)
        win.title(self.t("edit_customer_title"))
        win.geometry("450x350")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text=self.t("edit_customer_title"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 16, "bold")).pack(pady=10)
        f = tk.Frame(win, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        name_e = self.field(f, self.t("name"), c["name"])
        phone_e = self.phone_field(f, self.t("phone"), c["phone"] or "+60")
        email_e = self.email_field(f, self.t("email"), c["email"] or "")
        notes_e = self.field(f, self.t("notes"), c["notes"] or "")
        bf = tk.Frame(f, bg=C["bg"], pady=15)
        bf.pack(fill="x")
        def save():
            n = name_e.get().strip()
            if not n:
                return messagebox.showerror(self.t("error"), self.t("enter_name"))
            self.db.update_customer(c["id"], n, phone_e.get().strip(), email_e.get().strip(), c["address"], notes_e.get().strip())
            win.destroy()
            messagebox.showinfo(self.t("done"), self.t("customer_updated"))
            self._filter_custs()
        self.btn(bf, self.t("save"), save, bg=C["ok"]).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=win.destroy, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def pg_new_cust(self):
        self.clr()
        self.hdr(self.t("new_customer_title"))
        f = tk.Frame(self.content, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        self.ce = {}
        self.ce["Name"] = self.field(f, self.t("name"), "")
        self.ce["Phone"] = self.phone_field(f, self.t("phone"), "+60")
        self.ce["Email"] = self.email_field(f, self.t("email"), "")
        self.ce["Notes"] = self.field(f, self.t("notes"), "")
        bf = tk.Frame(f, bg=C["bg"], pady=20); bf.pack(fill="x")
        self.btn(bf, self.t("save"), self.save_cust).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=self.pg_custs, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def save_cust(self):
        n = self.ce["Name"].get().strip()
        if not n:
            return messagebox.showerror(self.t("error"), self.t("enter_name"))
        self.db.add_customer(n, self.ce["Phone"].get().strip(), self.ce["Email"].get().strip(), None, self.ce["Notes"].get().strip())
        messagebox.showinfo(self.t("done"), self.t("customer_saved"))
        self.pg_custs()

    def pg_cal(self):
        self.clr()
        self.hdr(self.t("appointments"), self.t("new_appointment"), self.pg_new_appt)
        f = tk.Frame(self.content, bg=C["bg"], padx=12)
        f.pack(fill="both", expand=True)
        sf = tk.Frame(f, bg=C["bg"])
        sf.pack(fill="x", pady=(0,10))
        self.appt_search_var = tk.StringVar()
        self.search_field(sf, self.t("search_appointments"), self.appt_search_var)
        self.appt_list_frame = tk.Frame(f, bg=C["bg"])
        self.appt_list_frame.pack(fill="both", expand=True)
        self.appt_search_var.trace("w", lambda *a: self._filter_appts())
        self._filter_appts()
        self.root.after(50, lambda: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))

    def _filter_appts(self):
        for w in self.appt_list_frame.winfo_children():
            w.destroy()
        q = self.appt_search_var.get().strip().lower()
        if q and q != self.t("search_appointments").lower():
            appts = self.db.search_appointments(q)
            if not appts:
                tk.Label(self.appt_list_frame, text=self.t("no_results"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
                return
        else:
            today = datetime.now().strftime("%Y-%m-%d")
            tk.Label(self.appt_list_frame, text=self.fmt_date(today), bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 12)).pack(anchor="w", pady=8)
            appts = self.db.get_appointments(today)
            if not appts:
                tk.Label(self.appt_list_frame, text=self.t("no_appointments"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
                return
        table = tk.Frame(self.appt_list_frame, bg=C["bg"])
        table.pack(fill="both", expand=True, padx=8)
        col_names = [self.t("date"), self.t("time"), self.t("customer"), self.t("purpose"), ""]
        col_wt = [1, 1, 2, 3, 0]
        col_minsize = [100, 70, 130, 180, 80]
        for i in range(5):
            table.grid_columnconfigure(i, weight=col_wt[i], minsize=col_minsize[i])
        for i, name in enumerate(col_names):
            if name:
                tk.Label(table, text=name, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10, "bold"), anchor="w", padx=4).grid(row=0, column=i, sticky="w", pady=(8, 4))
        for ri, a in enumerate(appts):
            row_bg = C["card"] if ri % 2 == 0 else C["bg"]
            row = ri + 1
            table.rowconfigure(row, pad=12)
            self.cell(table, self.fmt_date(a["date"]), font=("Segoe UI", 11), bg=row_bg, fg=C["txt2"]).grid(row=row, column=0, sticky="ew", padx=2)
            self.cell(table, a["time"], font=("Segoe UI", 11, "bold"), bg=row_bg, fg=C["txt"]).grid(row=row, column=1, sticky="ew", padx=2)
            self.cell(table, a["customer_name"] or self.t("walk_in"), font=("Segoe UI", 11, "bold"), bg=row_bg, fg=C["txt"], tooltip_text=a["customer_name"] or "").grid(row=row, column=2, sticky="ew", padx=2)
            self.cell(table, a["purpose"] or "-", font=("Segoe UI", 11), bg=row_bg, fg=C["txt2"], tooltip_text=a["purpose"] or "").grid(row=row, column=3, sticky="ew", padx=2)
            tk.Button(table, text=self.t("edit"), command=lambda a=a: self.edit_appt(a), bg=row_bg, fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, cursor="hand2").grid(row=row, column=4, sticky="e", padx=1)

    def edit_appt(self, a):
        win = tk.Toplevel(self.root)
        win.title(self.t("edit_appointment_title"))
        win.geometry("500x450")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text=self.t("edit_appointment_title"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 16, "bold")).pack(pady=10)
        f = tk.Frame(win, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        cust_name_e = self.field(f, self.t("customer"), a["customer_name"] or "")
        date_var = tk.StringVar(value=a["date"])
        date_frame = tk.Frame(f, bg=C["bg"])
        date_frame.pack(fill="x", pady=8)
        tk.Label(date_frame, text=self.t("date"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
        date_entry = tk.Entry(date_frame, textvariable=date_var, font=("Segoe UI", 12), bd=1, relief="solid", width=12)
        date_entry.pack(side="left")
        time_parts = a["time"].split(":") if a["time"] else ["09", "00"]
        hour_var = tk.StringVar(value=time_parts[0])
        min_var = tk.StringVar(value=time_parts[1] if len(time_parts) > 1 else "00")
        time_frame = tk.Frame(f, bg=C["bg"])
        time_frame.pack(fill="x", pady=8)
        tk.Label(time_frame, text=self.t("time"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 11, "bold"), width=20, anchor="w").pack(side="left")
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
                return messagebox.showerror(self.t("error"), self.t("cannot_empty"))
            t = f"{hour_var.get()}:{min_var.get()}"
            self.db.update_appointment(a["id"], d, t, purpose_e.get().strip(), a["status"], notes_e.get().strip())
            win.destroy()
            messagebox.showinfo(self.t("done"), self.t("appointment_updated"))
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
            return messagebox.showerror(self.t("error"), self.t("cannot_empty"))
        cid = None
        if c:
            cs = self.db.get_customers(c)
            cid = cs[0]["id"] if cs else self.db.add_customer(c)
        self.db.add_appointment(cid, d, t, self.ae["Purpose"].get().strip(), self.ae["Notes"].get().strip())
        messagebox.showinfo(self.t("done"), self.t("appointment_saved"))
        self.pg_cal()

    def pg_invs(self):
        self.clr()
        self.hdr(self.t("invoices"), self.t("from_job"), self.pg_new_inv)
        f = tk.Frame(self.content, bg=C["bg"], padx=12)
        f.pack(fill="both", expand=True)
        sf = tk.Frame(f, bg=C["bg"])
        sf.pack(fill="x", pady=(0,10))
        self.inv_search_var = tk.StringVar()
        self.search_field(sf, self.t("search_invoices"), self.inv_search_var)
        self.inv_list_frame = tk.Frame(f, bg=C["bg"])
        self.inv_list_frame.pack(fill="both", expand=True)
        self.inv_search_var.trace("w", lambda *a: self._filter_invs())
        self._filter_invs()
        self.root.after(50, lambda: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))

    def _filter_invs(self):
        for w in self.inv_list_frame.winfo_children():
            w.destroy()
        invs = self.db.get_invoices()
        q = self.inv_search_var.get().strip().lower()
        if q and q != self.t("search_invoices").lower():
            invs = [i for i in invs if q in (i["invoice_code"]+(i["customer_name"] or "")).lower()]
        if not invs:
            tk.Label(self.inv_list_frame, text=self.t("no_invoices") if not q else self.t("no_results"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=50)
            return
        unpaid = [i for i in invs if not i["paid"]]
        paid = [i for i in invs if i["paid"]]
        if unpaid:
            total_owed = sum(i["amount"] for i in unpaid)
            tk.Label(self.inv_list_frame, text=f"{self.t('unpaid')} ({len(unpaid)}, {self.fmt_amount(total_owed)})", bg=C["bg"], fg=C["err"], font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(8, 4), padx=8)
            table = tk.Frame(self.inv_list_frame, bg=C["bg"])
            table.pack(fill="both", expand=True, padx=8)
            col_names = [self.t("code"), self.t("customer"), self.t("amount"), "", "", "", ""]
            col_wt = [2, 3, 1, 0, 0, 0, 0]
            col_minsize = [130, 160, 90, 70, 70, 70, 70]
            for i in range(7):
                table.grid_columnconfigure(i, weight=col_wt[i], minsize=col_minsize[i])
            for i, name in enumerate(col_names):
                if name:
                    tk.Label(table, text=name, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10, "bold"), anchor="w", padx=4).grid(row=0, column=i, sticky="w", pady=(8, 4))
            for ri, inv in enumerate(unpaid):
                row_bg = "#FEF2F2" if ri % 2 == 0 else C["bg"]
                row = ri + 1
                table.rowconfigure(row, pad=12)
                self.cell(table, inv["invoice_code"], font=("Segoe UI", 11, "bold"), bg=row_bg, fg=C["txt"]).grid(row=row, column=0, sticky="ew", padx=2)
                self.cell(table, inv["customer_name"] or self.t("unknown"), font=("Segoe UI", 11), bg=row_bg, fg=C["txt"], tooltip_text=inv["customer_name"] or "").grid(row=row, column=1, sticky="ew", padx=2)
                self.cell(table, self.fmt_amount(inv['amount']), font=("Segoe UI", 11, "bold"), bg=row_bg, fg=C["err"]).grid(row=row, column=2, sticky="ew", padx=2)
                tk.Button(table, text=self.t("email"), command=lambda i=inv: self.send_email(i), bg="#2563EB", fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, cursor="hand2").grid(row=row, column=3, sticky="e", padx=1)
                tk.Button(table, text=self.t("wa"), command=lambda i=inv: self.send_whatsapp(i), bg=C["ok"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, cursor="hand2").grid(row=row, column=4, sticky="e", padx=1)
                tk.Button(table, text=self.t("pdf"), command=lambda i=inv: self.download_inv_pdf(i), bg="#7C3AED", fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, cursor="hand2").grid(row=row, column=5, sticky="e", padx=1)
                tk.Button(table, text=self.t("mark_paid"), command=lambda iid=inv["id"]: self.mark_paid(iid), bg=C["warn"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=6, cursor="hand2").grid(row=row, column=6, sticky="e", padx=1)
        if paid:
            tk.Label(self.inv_list_frame, text=f"{self.t('paid')} ({len(paid)})", bg=C["bg"], fg=C["ok"], font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(12, 4), padx=8)
            table2 = tk.Frame(self.inv_list_frame, bg=C["bg"])
            table2.pack(fill="both", expand=True, padx=8)
            col_names2 = [self.t("code"), self.t("customer"), self.t("amount"), self.t("method"), self.t("status")]
            col_wt2 = [2, 3, 1, 1, 1]
            col_minsize2 = [130, 160, 90, 90, 80]
            for i in range(5):
                table2.grid_columnconfigure(i, weight=col_wt2[i], minsize=col_minsize2[i])
            for i, name in enumerate(col_names2):
                tk.Label(table2, text=name, bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 10, "bold"), anchor="w", padx=4).grid(row=0, column=i, sticky="w", pady=(8, 4))
            for ri, inv in enumerate(paid):
                row_bg = C["card"] if ri % 2 == 0 else C["bg"]
                row = ri + 1
                table2.rowconfigure(row, pad=12)
                self.cell(table2, inv["invoice_code"], font=("Segoe UI", 11, "bold"), bg=row_bg, fg=C["txt"]).grid(row=row, column=0, sticky="ew", padx=2)
                self.cell(table2, inv["customer_name"] or self.t("unknown"), font=("Segoe UI", 11), bg=row_bg, fg=C["txt2"], tooltip_text=inv["customer_name"] or "").grid(row=row, column=1, sticky="ew", padx=2)
                self.cell(table2, self.fmt_amount(inv['amount']), font=("Segoe UI", 11, "bold"), bg=row_bg, fg=C["txt"]).grid(row=row, column=2, sticky="ew", padx=2)
                method = inv["payment_method"] or "-"
                method_bg = {"Cash": C["ok"], "E-Wallet": "#2563EB", "Card": "#7C3AED", "Transfer": C["warn"]}.get(method, C["txt3"])
                method_display = self.t(method.lower().replace("-","_")) if method and method != "-" else method
                tk.Label(table2, text=method_display, bg=method_bg, fg=C["white"], font=("Segoe UI", 10, "bold"), anchor="center", padx=4).grid(row=row, column=3, sticky="ew", padx=2)
                tk.Label(table2, text=self.t("paid_status"), bg=C["ok"], fg=C["white"], font=("Segoe UI", 10, "bold"), anchor="center", padx=4).grid(row=row, column=4, sticky="ew", padx=2)

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
        if pdf_path:
            messagebox.showinfo(self.t("done"), self.t("pdf_saved") + f"\n{pdf_path}")
            try:
                subprocess.run(["explorer", "/select,", pdf_path], check=False)
            except (OSError, FileNotFoundError):
                try:
                    os.startfile(os.path.dirname(pdf_path))
                except (OSError, AttributeError):
                    pass
        else:
            messagebox.showerror(self.t("error"), self.t("pdf_failed"))

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
            return messagebox.showwarning(self.t("no_phone_short"), self.t("no_phone"))
        use_pdf = self.db.get_setting("invoice_format", "text") == "pdf"
        pdf_path = None
        if use_pdf:
            pdf_path = self.generate_invoice_pdf(inv["invoice_code"], job_for_inv, cust)
        if use_pdf and pdf_path:
            msg = f"Hi {cust['name'] if cust else 'Customer'},\n\n"
            msg += f"Invoice {inv['invoice_code']} - {self.fmt_amount(inv['amount'])}\n"
            msg += f"Please find the attached PDF invoice.\n"
            thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
            msg += f"\n{thank_you}\n{self.db.get_setting('business_name', 'Shop')}"
            try:
                subprocess.run(["explorer", "/select,", pdf_path], check=False)
            except (OSError, FileNotFoundError):
                try:
                    os.startfile(os.path.dirname(pdf_path))
                except (OSError, AttributeError):
                    pass
        else:
            msg = f"Hi {cust['name'] if cust else 'Customer'},\n\n"
            msg += f"This is a friendly reminder for your unpaid invoice.\n\n"
            msg += f"Invoice: {inv['invoice_code']}\n"
            if job_for_inv:
                msg += f"Item: {job_for_inv['item']}\n"
                if job_for_inv['problem']:
                    msg += f"Service: {job_for_inv['problem']}\n"
            msg += f"Amount: {self.fmt_amount(inv['amount'])}\n\n"
            if job_for_inv and job_for_inv["due_date"]:
                msg += f"Due Date: {self.fmt_date(job_for_inv['due_date'])}\n"
            payment_terms = self.db.get_setting("payment_terms", "")
            if payment_terms:
                msg += f"{payment_terms}\n"
            msg += f"Please make payment at your convenience.\n\n"
            google_review = self.db.get_setting("google_review", "")
            if google_review:
                review_link = self.get_review_link(google_review)
                if review_link:
                    msg += f"\nWe'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
            thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
            msg += f"{thank_you}\n{self.db.get_setting('business_name', 'Shop')}"
        url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
        try:
            webbrowser.open(url)
        except (webbrowser.Error, OSError):
            pass
        if use_pdf and pdf_path:
            messagebox.showinfo(self.t("done"), self.t("opening_whatsapp") + f" +{phone}\n{self.t('pdf_opened')}")
        else:
            messagebox.showinfo(self.t("done"), self.t("opening_whatsapp") + f" +{phone}")

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
            return messagebox.showwarning(self.t("no_email_short"), self.t("no_email"))
        biz_name = self.db.get_setting('business_name', 'Shop')
        subject = f"Invoice {inv['invoice_code']} from {biz_name}"
        use_pdf = self.db.get_setting("invoice_format", "text") == "pdf"
        pdf_path = None
        if use_pdf:
            pdf_path = self.generate_invoice_pdf(inv["invoice_code"], job_for_inv, cust)
        if use_pdf and pdf_path:
            body = f"Dear {cust['name'] if cust else 'Customer'},\n\n"
            body += f"Please find attached invoice {inv['invoice_code']}.\n\n"
            if job_for_inv and job_for_inv["due_date"]:
                body += f"Due Date: {self.fmt_date(job_for_inv['due_date'])}\n"
            payment_terms = self.db.get_setting("payment_terms", "")
            if payment_terms:
                body += f"{payment_terms}\n"
            body += f"Amount: {self.fmt_amount(inv['amount'])}\n\n"
            google_review = self.db.get_setting("google_review", "")
            if google_review:
                review_link = self.get_review_link(google_review)
                if review_link:
                    body += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
            thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
            body += f"{thank_you}\n{biz_name}"
            mailto = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            try:
                webbrowser.open(mailto)
                os.startfile(pdf_path)
            except (webbrowser.Error, OSError):
                pass
            messagebox.showinfo(self.t("done"), self.t("email_opened") + f" {email}\n{self.t('pdf_saved')} {pdf_path}")
        else:
            body = f"Dear {cust['name'] if cust else 'Customer'},\n\n"
            thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
            body += f"{thank_you}\n\n"
            body += f"Invoice: {inv['invoice_code']}\n"
            body += f"Date: {self.fmt_date(datetime.now().strftime('%Y-%m-%d'))}\n"
            if job_for_inv:
                body += f"Item: {job_for_inv['item']}\n"
                body += f"Service: {job_for_inv['problem'] or 'N/A'}\n"
            body += f"Amount: {self.fmt_amount(inv['amount'])}\n"
            if job_for_inv and job_for_inv["due_date"]:
                body += f"Due Date: {self.fmt_date(job_for_inv['due_date'])}\n"
            payment_terms = self.db.get_setting("payment_terms", "")
            if payment_terms:
                body += f"{payment_terms}\n"
            body += f"Status: UNPAID\n\n"
            body += f"Please make payment at your earliest convenience.\n\n"
            google_review = self.db.get_setting("google_review", "")
            if google_review:
                review_link = self.get_review_link(google_review)
                if review_link:
                    body += f"We'd love your feedback! Leave us a Google review:\n{review_link}\n\n"
            body += f"{thank_you}\n{biz_name}"
            mailto = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            try:
                webbrowser.open(mailto)
            except (webbrowser.Error, OSError):
                pass
            messagebox.showinfo(self.t("done"), self.t("opening_email") + f" {email}")

    def generate_invoice_pdf(self, inv_code, job, cust):
        try:
            invoice_dir = os.path.join(APP_DIR, "data", "invoices")
            os.makedirs(invoice_dir, exist_ok=True)
            pdf = FPDF()
            pdf.add_page()
            invoice_title = self.db.get_setting("invoice_title", "INVOICE")
            pdf.set_font("Helvetica", "B", 22)
            pdf.cell(0, 12, invoice_title, new_x="LMARGIN", new_y="NEXT", align="R")
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, f"Invoice: {inv_code}", new_x="LMARGIN", new_y="NEXT", align="R")
            pdf.cell(0, 6, f"Date: {self.fmt_date(datetime.now().strftime('%Y-%m-%d'))}", new_x="LMARGIN", new_y="NEXT", align="R")
            if job and job["due_date"]:
                pdf.cell(0, 6, f"Due Date: {self.fmt_date(job['due_date'])}", new_x="LMARGIN", new_y="NEXT", align="R")
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
            pdf.cell(60, 8, "  Item", border=1, fill=True)
            pdf.cell(75, 8, "  Service / Problem", border=1, fill=True)
            pdf.cell(35, 8, "  Amount", border=1, new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "", 10)
            item = job["item"] if job else "N/A"
            problem = (job["problem"] or "N/A") if job else "N/A"
            item_lines = pdf.multi_cell(60, 6, f"  {item}", split_only=True)
            prob_lines = pdf.multi_cell(75, 6, f"  {problem}", split_only=True)
            max_lines = max(len(item_lines), len(prob_lines), 1)
            row_h = max_lines * 6
            x_start = pdf.get_x()
            y_start = pdf.get_y()
            pdf.multi_cell(60, row_h, f"  {item}", border=1)
            pdf.set_xy(x_start + 60, y_start)
            pdf.multi_cell(75, row_h, f"  {problem}", border=1)
            pdf.set_xy(x_start + 135, y_start)
            amount_text = f"  {self.fmt_amount(job['quote'])}" if job else "  RM 0.00"
            pdf.cell(35, row_h, amount_text, border=1, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(135, 10, "Total:", border=1)
            pdf.cell(35, 10, self.fmt_amount(job['quote']) if job else "RM 0.00", border=1, new_x="LMARGIN", new_y="NEXT")
            payment_terms = self.db.get_setting("payment_terms", "")
            if payment_terms:
                pdf.ln(5)
                pdf.set_font("Helvetica", "", 10)
                pdf.cell(0, 6, payment_terms, new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.ln(5)
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
            thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
            if thank_you:
                pdf.set_font("Helvetica", "", 10)
                pdf.cell(0, 6, thank_you, new_x="LMARGIN", new_y="NEXT", align="C")
            footer_text = self.db.get_setting("footer_text", "")
            if footer_text:
                pdf.set_font("Helvetica", "", 8)
                pdf.cell(0, 6, footer_text, new_x="LMARGIN", new_y="NEXT", align="C")
            filename = f"{inv_code}.pdf"
            filepath = os.path.join(invoice_dir, filename)
            pdf.output(filepath)
            self.cleanup_old_pdfs(invoice_dir)
            return filepath
        except Exception as e:
            messagebox.showerror(self.t("pdf_error"), self.t("pdf_failed"))
            return None

    def cleanup_old_pdfs(self, invoice_dir):
        try:
            now = time.time()
            cutoff = now - (7 * 24 * 60 * 60)
            deleted = 0
            for f in os.listdir(invoice_dir):
                if f.endswith(".pdf"):
                    fp = os.path.join(invoice_dir, f)
                    if os.path.getmtime(fp) < cutoff:
                        os.remove(fp)
                        deleted += 1
            if deleted > 0:
                messagebox.showinfo(self.t("done"), f"{self.t('cleanup')} {deleted} {self.t('cleanup_msg')}")
        except Exception:
            pass

    def mark_paid(self, iid):
        win = tk.Toplevel(self.root)
        win.title(self.t("payment_title"))
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
            tk.Label(r, text=self.fmt_amount(j['quote']), bg=C["card"], fg=C["txt"], font=("Segoe UI", 11, "bold"), anchor="w", padx=15).pack(side="left")
            tk.Button(r, text=self.t("create"), command=lambda j=j: [self.db.add_invoice(j["id"], j["quote"]), messagebox.showinfo(self.t("done"), self.t("invoice_created")), self.pg_invs()], bg=C["pri"], fg=C["white"], font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2").pack(side="right")

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
            (self.t("today"), self.fmt_amount(today_rev), self.t("collected_today"), C["ok"]),
            (self.t("this_week"), self.fmt_amount(week_rev), self.t("collected_week"), C["ok"]),
            (self.t("this_month"), self.fmt_amount(month_rev), self.t("collected_month"), C["ok"]),
            (self.t("owed"), self.fmt_amount(outstanding), self.t("owed_desc"), C["err"] if outstanding > 0 else C["ok"]),
        ]
        for i, (title, value, desc, color) in enumerate(cards):
            c = tk.Frame(sf, bg=C["card"], bd=1, relief="solid", pady=10, padx=12)
            c.grid(row=0, column=i, padx=4, pady=8, sticky="nsew")
            tk.Label(c, text=title, bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9)).pack(anchor="w")
            tk.Label(c, text=value, bg=C["card"], fg=color, font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=3)
            tk.Label(c, text=desc, bg=C["card"], fg=C["txt3"], font=("Segoe UI", 8)).pack(anchor="w")
        for i in range(4):
            sf.columnconfigure(i, weight=1)
        st = tk.Frame(self.content, bg=C["bg"], padx=20, pady=15)
        st.pack(fill="both", expand=True)
        tk.Label(st, text=self.t("summary"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=10)
        summary = [
            (self.t("total_earned"), self.fmt_amount(total_earned), C["ok"]),
            (self.t("outstanding_unpaid"), self.fmt_amount(outstanding), C["err"] if outstanding > 0 else C["ok"]),
            (self.t("total_jobs"), str(len(jobs)), C["txt"]),
            (self.t("completed_jobs"), str(len([j for j in jobs if j["status"]=="done"])), C["ok"]),
            (self.t("active_jobs_count"), str(len([j for j in jobs if j["status"]!="done"])), C["warn"]),
            (self.t("total_customers"), str(len(self.db.get_customers())), C["txt"]),
            (self.t("paid_invoices_count"), str(len(paid)), C["ok"]),
            (self.t("unpaid_invoices_count"), str(len(unpaid)), C["err"] if unpaid else C["ok"]),
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
            tk.Label(self.srch_r, text=f"{self.t('no_results_for')} '{q}'", bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 14)).pack(pady=40)
            return
        tk.Label(self.srch_r, text=f"{t} {self.t('results_count')} '{q}'", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=8)
        if fj:
            tk.Label(self.srch_r, text=f"{self.t('jobs_header')} ({len(fj)})", bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=8)
            for j in fj:
                r = self.row(self.srch_r)
                tk.Label(r, text=f"{j['job_code']} - {j['item']}", bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(side="left")
                tk.Label(r, text=self.t(j["status"].replace("-","_")), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), padx=10).pack(side="left")
                tk.Label(r, text=f"{self.t('id_label')} {j['id']}", bg=C["card"], fg=C["txt3"], font=("Segoe UI", 9), padx=10).pack(side="left")
        if fc:
            tk.Label(self.srch_r, text=f"{self.t('customers_header')} ({len(fc)})", bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=8)
            for c in fc:
                r = self.row(self.srch_r)
                tk.Label(r, text=c["name"], bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(side="left")
                tk.Label(r, text=c["phone"] or "", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10), padx=10).pack(side="left")
                if c["email"]:
                    tk.Label(r, text=c["email"], bg=C["card"], fg=C["txt3"], font=("Segoe UI", 9), padx=10).pack(side="left")
                tk.Label(r, text=f"{self.t('id_label')} {c['id']}", bg=C["card"], fg=C["txt3"], font=("Segoe UI", 9), padx=10).pack(side="left")
        if fi:
            tk.Label(self.srch_r, text=f"{self.t('invoices_header')} ({len(fi)})", bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=8)
            for i in fi:
                r = self.row(self.srch_r)
                tk.Label(r, text=f"{i['invoice_code']} - {self.fmt_amount(i['amount'])}", bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(side="left")
                s = self.t("paid_status") if i["paid"] else self.t("unpaid_status")
                co = C["ok"] if i["paid"] else C["err"]
                tk.Label(r, text=s, bg=co, fg=C["white"], font=("Segoe UI", 9, "bold"), padx=8, pady=2).pack(side="right")

    def pg_backup(self):
        self.clr()
        self.hdr(self.t("backup"))
        f = tk.Frame(self.content, bg=C["bg"], padx=20)
        f.pack(fill="both", expand=True)
        s1 = self.row(f)
        tk.Label(s1, text=self.t("full_backup"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(s1, text=self.t("backup_desc"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        bf1 = tk.Frame(s1, bg=C["card"])
        bf1.pack(fill="x", pady=5)
        self.btn(bf1, self.t("backup_now"), self.do_backup, bg=C["ok"]).pack(side="left", padx=5)
        self.btn(bf1, self.t("restore_backup"), self.do_restore, bg=C["warn"]).pack(side="left", padx=5)
        s2 = self.row(f)
        tk.Label(s2, text=self.t("export_csv_section"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        for l, fn, g, tk_key in [("Customers","customers.csv",lambda:self.db.get_customers(), "export_customers"),("Jobs","jobs.csv",lambda:self.db.get_jobs(), "export_jobs"),("Invoices","invoices.csv",lambda:self.db.get_invoices(), "export_invoices")]:
            r = tk.Frame(s2, bg=C["card"])
            r.pack(fill="x", pady=3)
            tk.Label(r, text=l, bg=C["card"], fg=C["txt"], font=("Segoe UI", 11), anchor="w").pack(side="left")
            tk.Button(r, text=self.t(tk_key), command=lambda fn=fn,g=g: self.do_export(fn,g), bg=C["pri"], fg=C["white"], font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=4, cursor="hand2").pack(side="right")

    def do_backup(self):
        from tkinter import filedialog
        db_path = os.path.join(APP_DIR, "data", "data.db")
        if not os.path.exists(db_path):
            return messagebox.showerror(self.t("error"), self.t("no_backup"))
        default_name = f"kerjamudah_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        fp = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database","*.db")], initialfile=default_name)
        if not fp:
            return
        import shutil
        try:
            shutil.copy2(db_path, fp)
            messagebox.showinfo(self.t("backup_complete"), self.t("backup_complete") + f":\n{fp}")
        except Exception as e:
            messagebox.showerror(self.t("error"), self.t("backup_failed"))

    def do_restore(self):
        from tkinter import filedialog
        fp = filedialog.askopenfilename(filetypes=[("Database","*.db")])
        if not fp:
            return
        if not messagebox.askyesno(self.t("confirm_restore_title"), self.t("confirm_restore_msg")):
            return
        import shutil
        db_path = os.path.join(APP_DIR, "data", "data.db")
        try:
            shutil.copy2(fp, db_path)
            self.db.close()
            self.db = Database(db_path)
            messagebox.showinfo(self.t("done"), self.t("restore_complete"))
            self.layout()
        except Exception as e:
            messagebox.showerror(self.t("error"), self.t("restore_failed"))

    def do_export(self, fn, g):
        from tkinter import filedialog, csv
        data = g()
        if not data:
            return messagebox.showinfo(self.t("done"), self.t("nothing_export"))
        fp = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile=fn)
        if not fp:
            return
        try:
            with open(fp, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                keys = list(data[0].keys())
                w.writerow(keys)
                for row in data:
                    w.writerow([row[k] for k in keys])
            messagebox.showinfo(self.t("done"), self.t("exported") + f" {fp}")
        except Exception as e:
            messagebox.showerror(self.t("error"), self.t("nothing_export"))

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
            tk.Button(r, text=self.t("edit"), command=cmd, bg=C["card"], fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=8, cursor="hand2").pack(side="right")
        s_gr = self.row(f)
        tk.Label(s_gr, text=self.t("google_review"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(s_gr, text=self.t("add_google_maps"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        gr_val = self.db.get_setting("google_review", "")
        gr_frame = tk.Frame(s_gr, bg=C["card"])
        gr_frame.pack(fill="x", pady=5)
        gr_display = gr_val if gr_val else self.t("not_set")
        tk.Label(gr_frame, text=f"{self.t('maps_link_label')} {gr_display}", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 11)).pack(side="left")
        tk.Button(gr_frame, text=self.t("edit"), command=self.edit_google_review, bg=C["card"], fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=8, cursor="hand2").pack(side="right")
        tk.Label(s_gr, text=self.t("google_maps_instructions"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10,2))
        tk.Label(s_gr, text=self.t("google_maps_step1"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text=self.t("google_maps_step2"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text=self.t("google_maps_step3"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text=self.t("google_maps_step4"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text=self.t("google_maps_step5"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 9), anchor="w").pack(fill="x")
        tk.Label(s_gr, text="", bg=C["card"], font=("Segoe UI", 6)).pack()
        tk.Label(s_gr, text=self.t("example_link"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5,2))
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
        tk.Label(s3, text=self.t("language"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        lf = tk.Frame(s3, bg=C["card"])
        lf.pack(fill="x", pady=5)
        self.lang_var = tk.StringVar(value=self.lang)
        for v, t in [("en","English"),("ms","Bahasa Malaysia"),("zh","Chinese")]:
            tk.Radiobutton(lf, text=t, variable=self.lang_var, value=v, bg=C["card"], font=("Segoe UI", 11)).pack(side="left", padx=10)
        self.btn(s3, self.t("save"), self.change_lang, bg=C["ok"]).pack(anchor="w", pady=5)
        s_inv = self.row(f)
        tk.Label(s_inv, text=self.t("invoice_format"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(s_inv, text=self.t("choose_format"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        ifr = tk.Frame(s_inv, bg=C["card"])
        ifr.pack(fill="x", pady=5)
        self.inv_fmt_var = tk.StringVar(value=self.db.get_setting("invoice_format", "text"))
        tk.Radiobutton(ifr, text=self.t("text_plain"), variable=self.inv_fmt_var, value="text", bg=C["card"], font=("Segoe UI", 11)).pack(side="left", padx=10)
        tk.Radiobutton(ifr, text=self.t("pdf_professional"), variable=self.inv_fmt_var, value="pdf", bg=C["card"], font=("Segoe UI", 11)).pack(side="left", padx=10)
        self.btn(s_inv, self.t("save"), self.save_inv_fmt, bg=C["ok"]).pack(anchor="w", pady=5)
        self.btn(s_inv, self.t("preview_invoice"), self.preview_invoice, bg="#2563EB").pack(anchor="w", pady=5)
        s5 = self.row(f)
        tk.Label(s5, text=self.t("startup"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(s5, text=self.t("open_on_startup"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        shortcut_path = os.path.join(startup_folder, "Kerja Mudah.bat")
        is_enabled = os.path.exists(shortcut_path)
        status_text = self.t("on_startup") if is_enabled else self.t("off_startup")
        status_color = C["ok"] if is_enabled else C["txt2"]
        tk.Label(s5, text=f"{self.t('status')}: {status_text}", bg=C["card"], fg=status_color, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=2)
        self.btn(s5, self.t("toggle_startup"), self.toggle_startup, bg=C["warn"]).pack(anchor="w", pady=5)
        s6 = self.row(f)
        tk.Label(s6, text=self.t("invoice_parameters"), bg=C["card"], fg=C["txt"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(s6, text=self.t("customize_invoice"), bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        params = [
            (self.t("invoice_title"), "invoice_title", "INVOICE", 50),
            (self.t("payment_terms"), "payment_terms", "Payment due upon receipt", 150),
            (self.t("thank_you_note"), "thank_you_note", "Thank you for your business!", 150),
            (self.t("footer_text"), "footer_text", "", 200),
        ]
        for label_text, key, default_val, max_len in params:
            pf = tk.Frame(s6, bg=C["card"])
            pf.pack(fill="x", pady=3)
            val = self.db.get_setting(key, default_val)
            tk.Label(pf, text=f"{label_text}: {val if val else self.t('empty_placeholder')}", bg=C["card"], fg=C["txt2"], font=("Segoe UI", 10)).pack(side="left")
            tk.Button(pf, text=self.t("edit"), command=lambda k=key, l=label_text, m=max_len: self._edit_invoice_param(k, l, m), bg=C["card"], fg=C["pri"], font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=8, cursor="hand2").pack(side="right")
        self.content.update_idletasks()
        self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))

    def toggle_startup(self):
        startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        shortcut_path = os.path.join(startup_folder, "Kerja Mudah.bat")
        try:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                messagebox.showinfo(self.t("done"), self.t("startup_removed"))
            else:
                if getattr(sys, 'frozen', False):
                    exe_path = sys.executable
                else:
                    exe_path = os.path.abspath(sys.argv[0])
                bat_content = f'@echo off\nstart "" "{exe_path}"'
                with open(shortcut_path, "w") as f:
                    f.write(bat_content)
                messagebox.showinfo(self.t("done"), self.t("startup_updated"))
        except Exception as e:
            messagebox.showerror(self.t("error"), self.t("startup_error"))

    def preview_invoice(self):
        win = tk.Toplevel(self.root)
        win.title(self.t("preview_invoice"))
        win.geometry("500x650")
        win.configure(bg=C["white"])
        win.grab_set()
        canvas = tk.Canvas(win, bg=C["white"], highlightthickness=0)
        scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=C["white"])
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        biz_name = self.db.get_setting("business_name", "Your Business")
        biz_phone = self.db.get_setting("business_phone", "")
        biz_email = self.db.get_setting("business_email", "")
        google_review = self.db.get_setting("google_review", "")
        inv_title = self.db.get_setting("invoice_title", "INVOICE")
        payment_terms = self.db.get_setting("payment_terms", "Payment due upon receipt")
        thank_you = self.db.get_setting("thank_you_note", "Thank you for your business!")
        footer = self.db.get_setting("footer_text", "")
        inv_fmt = self.db.get_setting("invoice_format", "text")
        tk.Label(scroll_frame, text=biz_name, bg=C["white"], fg=C["txt"], font=("Segoe UI", 20, "bold")).pack(pady=(20,5))
        tk.Label(scroll_frame, text=inv_title, bg=C["white"], fg=C["txt3"], font=("Segoe UI", 14)).pack()
        tk.Frame(scroll_frame, bg=C["bdr"], height=2).pack(fill="x", padx=30, pady=15)
        tk.Label(scroll_frame, text="Invoice #: INV-DEMO-001", bg=C["white"], fg=C["txt2"], font=("Segoe UI", 11), anchor="w").pack(fill="x", padx=40)
        tk.Label(scroll_frame, text=f"Date: {datetime.now().strftime('%d %B %Y')}", bg=C["white"], fg=C["txt2"], font=("Segoe UI", 11), anchor="w").pack(fill="x", padx=40)
        tk.Label(scroll_frame, text="", bg=C["white"], font=("Segoe UI", 6)).pack()
        tk.Label(scroll_frame, text=self.t("bill_to"), bg=C["white"], fg=C["txt3"], font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", padx=40)
        tk.Label(scroll_frame, text="Customer Name", bg=C["white"], fg=C["txt"], font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x", padx=40)
        tk.Label(scroll_frame, text="+60 12-345 6789", bg=C["white"], fg=C["txt2"], font=("Segoe UI", 11), anchor="w").pack(fill="x", padx=40)
        tk.Frame(scroll_frame, bg=C["bdr"], height=1).pack(fill="x", padx=30, pady=10)
        tk.Label(scroll_frame, text="Item", bg=C["white"], fg=C["txt3"], font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", padx=40)
        tk.Label(scroll_frame, text="iPhone 15 Pro Screen Replacement", bg=C["white"], fg=C["txt"], font=("Segoe UI", 11), anchor="w").pack(fill="x", padx=40)
        tk.Label(scroll_frame, text="Service: Replace cracked screen", bg=C["white"], fg=C["txt2"], font=("Segoe UI", 10), anchor="w").pack(fill="x", padx=40)
        tk.Frame(scroll_frame, bg=C["bdr"], height=1).pack(fill="x", padx=30, pady=10)
        tk.Label(scroll_frame, text=f"{self.t('total')} RM 450", bg=C["white"], fg=C["txt"], font=("Segoe UI", 16, "bold"), anchor="e").pack(fill="x", padx=40)
        if payment_terms:
            tk.Label(scroll_frame, text=payment_terms, bg=C["white"], fg=C["txt2"], font=("Segoe UI", 10), anchor="w").pack(fill="x", padx=40, pady=(5,0))
        tk.Frame(scroll_frame, bg=C["bdr"], height=2).pack(fill="x", padx=30, pady=15)
        if biz_phone:
            tk.Label(scroll_frame, text=f"{self.t('phone_label')} {biz_phone}", bg=C["white"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", padx=40)
        if biz_email:
            tk.Label(scroll_frame, text=f"{self.t('email_label')} {biz_email}", bg=C["white"], fg=C["txt2"], font=("Segoe UI", 10)).pack(anchor="w", padx=40)
        if google_review:
            tk.Label(scroll_frame, text=self.t("rate_us"), bg=C["white"], fg=C["txt3"], font=("Segoe UI", 9)).pack(anchor="w", padx=40, pady=(10,2))
        if thank_you:
            tk.Label(scroll_frame, text=thank_you, bg=C["white"], fg=C["txt"], font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=40, pady=(10,2))
        if footer:
            tk.Label(scroll_frame, text=footer, bg=C["white"], fg=C["txt3"], font=("Segoe UI", 9)).pack(anchor="w", padx=40, pady=(5,0))
        fmt_label = f"Format: {inv_fmt.upper()}"
        tk.Label(scroll_frame, text=fmt_label, bg=C["white"], fg=C["txt3"], font=("Segoe UI", 8)).pack(anchor="w", padx=40, pady=(10,0))
        tk.Button(scroll_frame, text=self.t("close"), command=win.destroy, bg=C["card"], fg=C["txt"], font=("Segoe UI", 10), bd=1, relief="solid", padx=15, cursor="hand2").pack(pady=15)

    def edit_biz_name(self):
        self._edit_biz_field("business_name", self.t("business_name"))

    def edit_biz_phone(self):
        self._edit_biz_field("business_phone", self.t("phone"))

    def edit_biz_email(self):
        self._edit_biz_field("business_email", self.t("email"))

    def edit_google_review(self):
        self._edit_biz_field("google_review", self.t("google_review"))

    def _edit_biz_field(self, field, label):
        if self.db.get_setting("pin_hash"):
            self._pending_biz_edit = field
            self._pending_biz_label = label
            self._verify_pin_for_edit()
        else:
            self._show_biz_edit_dialog(field, label)

    def _verify_pin_for_edit(self):
        win = tk.Toplevel(self.root)
        win.title(self.t("verify"))
        win.geometry("300x180")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text=self.t("enter_pin_to_edit"), bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(pady=15)
        pin_e = tk.Entry(win, font=("Segoe UI", 14), bd=1, relief="solid", width=10, justify="center", show="*")
        pin_e.pack(pady=5)
        pin_e.focus()
        def verify():
            if self.h(pin_e.get().strip()) == self.db.get_setting("pin_hash"):
                win.destroy()
                self._show_biz_edit_dialog(self._pending_biz_edit, self._pending_biz_label)
            else:
                messagebox.showerror(self.t("error"), self.t("wrong_pin"))
                pin_e.delete(0, tk.END)
        pin_e.bind("<Return>", lambda e: verify())
        self.btn(win, self.t("verify"), verify).pack(pady=10)

    def _show_biz_edit_dialog(self, field, label):
        win = tk.Toplevel(self.root)
        win.title(f"{self.t('edit')} {label}")
        win.geometry("350x180")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text=f"{self.t('new_prefix')} {label}:", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(pady=15)
        if field == "google_review":
            tk.Label(win, text=self.t("maps_link_paste"), bg=C["bg"], fg=C["txt3"], font=("Segoe UI", 9)).pack(padx=25, anchor="w")
        e = tk.Entry(win, font=("Segoe UI", 14), bd=1, relief="solid", width=25)
        e.insert(0, self.db.get_setting(field, ""))
        e.pack(pady=5)
        e.focus()
        def save():
            val = e.get().strip()
            if not val:
                return messagebox.showerror(self.t("error"), self.t("cannot_empty"))
            if field == "google_review":
                valid = False
                lower = val.lower()
                if "g.page" in lower or "google.com/maps" in lower or "search.google.com/local" in lower or "maps.app.goo.gl" in lower:
                    valid = True
                if not valid:
                    return messagebox.showerror(self.t("error"), self.t("invalid_google_link"))
            self.db.set_setting(field, val)
            win.destroy()
            messagebox.showinfo(self.t("done"), f"{label} {self.t('label_updated')}")
            self.pg_set()
        e.bind("<Return>", lambda e: save())
        self.btn(win, self.t("save"), save, bg=C["ok"]).pack(pady=10)

    def _edit_invoice_param(self, key, label, max_len=200):
        win = tk.Toplevel(self.root)
        win.title(f"{self.t('edit')} {label}")
        win.geometry("400x180")
        win.configure(bg=C["bg"])
        win.grab_set()
        tk.Label(win, text=f"{label}:", bg=C["bg"], fg=C["txt"], font=("Segoe UI", 12, "bold")).pack(pady=15)
        e = tk.Entry(win, font=("Segoe UI", 12), bd=1, relief="solid", width=30)
        e.insert(0, self.db.get_setting(key, ""))
        e.pack(pady=5)
        e.focus()
        def save():
            self.db.set_setting(key, e.get().strip())
            win.destroy()
            messagebox.showinfo(self.t("done"), f"{label} {self.t('updated_suffix')}")
            self.pg_set()
        e.bind("<Return>", lambda e: save())
        self.btn(win, self.t("save"), save, bg=C["ok"]).pack(pady=10)

    def pg_set_pin(self):
        self.clr()
        self.hdr(self.t("set_pin"))
        f = tk.Frame(self.content, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        self.sp1 = self.pin_field(f, self.t("pin_4_digits"))
        self.sp2 = self.pin_field(f, self.t("confirm_pin"))
        bf = tk.Frame(f, bg=C["bg"], pady=20); bf.pack(fill="x")
        self.btn(bf, self.t("save"), self.save_pin).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=self.pg_set, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def save_pin(self):
        p = self.sp1.get().strip()
        c = self.sp2.get().strip()
        if len(p) != 4 or not p.isdigit():
            return messagebox.showerror(self.t("error"), self.t("pin_digits"))
        if p != c:
            return messagebox.showerror(self.t("error"), self.t("pins_match"))
        self.db.set_setting("pin_hash", self.h(p))
        messagebox.showinfo(self.t("done"), self.t("pin_set"))
        self.pg_set()

    def pg_chg_pin(self):
        self.clr()
        self.hdr(self.t("change_pin"))
        f = tk.Frame(self.content, bg=C["bg"], padx=25)
        f.pack(fill="both", expand=True)
        self.cp1 = self.pin_field(f, self.t("current_pin"))
        self.cp2 = self.pin_field(f, self.t("new_pin"))
        self.cp3 = self.pin_field(f, self.t("confirm_new_pin"))
        bf = tk.Frame(f, bg=C["bg"], pady=20); bf.pack(fill="x")
        self.btn(bf, self.t("save"), self.save_chg_pin).pack(side="left")
        tk.Button(bf, text=self.t("cancel"), command=self.pg_set, bg=C["bg"], fg=C["txt2"], font=("Segoe UI", 11), bd=1, relief="solid", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)

    def save_chg_pin(self):
        o = self.cp1.get().strip()
        n = self.cp2.get().strip()
        c = self.cp3.get().strip()
        if self.h(o) != self.db.get_setting("pin_hash"):
            return messagebox.showerror(self.t("error"), self.t("wrong_current_pin"))
        if len(n) != 4 or not n.isdigit():
            return messagebox.showerror(self.t("error"), self.t("new_pin_digits"))
        if n != c:
            return messagebox.showerror(self.t("error"), self.t("pins_match"))
        self.db.set_setting("pin_hash", self.h(n))
        messagebox.showinfo(self.t("done"), self.t("pin_changed"))
        self.pg_set()

    def rm_pin(self):
        if messagebox.askyesno(self.t("confirm"), self.t("remove_pin_confirm")):
            self.db.remove_setting("pin_hash")
            messagebox.showinfo(self.t("done"), self.t("pin_removed"))
            self.pg_set()

    def save_inv_fmt(self):
        fmt = self.inv_fmt_var.get()
        self.db.set_setting("invoice_format", fmt)
        messagebox.showinfo(self.t("done"), self.t("invoice_format_set") + f" {fmt.upper()}")
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
