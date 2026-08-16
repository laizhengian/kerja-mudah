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
- [x] `send_pickup_reminder` phone validation — empty phone check moved before "60" prefix
- [x] `invs[-1]` — guarded with `if invs else None` (not a crash)
- [x] `pdf_path` None crash in `download_inv_pdf` — added null check
- [x] All `webbrowser.open()` calls wrapped in try/except
- [x] All `os.startfile()` calls wrapped in try/except

### 1.2 Database Issues
- [x] All queries use parameterized statements (no SQL injection)
- [x] WAL mode enabled — prevents "database is locked" errors
- [x] `busy_timeout=5000` set — handles concurrent access
- [x] `_next_job_number()` race condition — retry with IntegrityError catch
- [x] `_next_invoice_number()` same fix
- [x] `remove_setting()` method added — `rm_pin` no longer bypasses Database class
- [ ] No migration system — schema changes require manual SQL (acceptable for v1)

### 1.3 Potential Data Loss
- [-] No delete records — prevents accidental loss (acceptable for v1)
- [-] No undo (acceptable for v1)
- [-] `cleanup_old_invoices()` deletes paid invoices >7 days — user is warned

---

## 2. HIGH — Broken Feature / Wrong Behavior

### 2.1 Search/Filter Bugs
- [x] Search filters use `self.t("search_*")` instead of hardcoded English placeholders
- [x] `_filter_invs()` called once (removed duplicate)

### 2.2 Scroll Issues
- [x] `pg_home()` — scroll region updated after rebuild
- [x] `pg_jobs()` — scroll region updated after rebuild
- [x] `pg_custs()` — scroll region updated after rebuild
- [x] `pg_cal()` — scroll region updated after rebuild
- [x] `pg_invs()` — scroll region updated after rebuild
- [x] `pg_set()` — scroll region updated after rebuild

### 2.3 Translation Gaps — UI Labels
- [x] "WA" button uses `self.t("wa")`
- [x] Status badges use `self.t(status)` instead of `.upper()`
- [x] Edit dialog titles use `self.t("edit")` instead of hardcoded "Edit"
- [x] Cleanup message uses `self.t("cleanup")` + `self.t("cleanup_msg")`

### 2.4 Translation Gaps — Customer-Facing Messages
- [~] WhatsApp message templates are English-only (acceptable for v1)
- [~] Email templates are English-only (acceptable for v1)
- [~] PDF labels are English-only (acceptable for v1)
- [x] Payment method display translated via `self.t()`

### 2.5 Payment Methods
- [x] Payment method labels translated in invoice list
- [-] DB stores English strings — translating would require data migration (acceptable for v1)

---

## 3. MEDIUM — Security / Best Practice

### 3.1 Security
- [-] PIN is SHA256(pin) without salt — only 10,000 possible PINs (acceptable for local desktop)
- [-] License key is SHA256(HWID)[:20] — weak but acceptable for small business
- [-] HWID is spoofable — acceptable for small business
- [x] Exception details no longer shown to users (PDF, backup, restore, export, startup errors)
- [x] No secrets in source code
- [x] `.gitignore` excludes sensitive files

### 3.2 Error Handling
- [x] `sqlite3.connect()` has timeout=10
- [x] WAL mode + busy_timeout handles concurrent access
- [x] All user-facing errors use translated safe messages
- [x] `rm_pin` uses Database class API

### 3.3 Thread Safety
- [x] WAL mode reduces lock contention
- [x] busy_timeout handles concurrent access
- [-] Single connection shared — acceptable for single-threaded Tkinter app

---

## 4. LOW — UX Polish / Performance

### 4.1 Input Validation
- [x] `field()` validates max_len
- [x] `name_field()` blocks dangerous chars, max 50
- [x] `phone_field()` digits/+-, max 20
- [x] `email_field()` blocks dangerous chars, max 80
- [x] `pin_field()` 4 digits only
- [x] `number_field()` digits/.-, max 12
- [x] `date_field()` month 1-12, day 1-31
- [x] `text_area_field()` max_len + character filtering
- [x] Phone field in `pg_new_job` max 20 chars
- [x] Email field in `pg_new_job` has validation
- [-] `edit_appt` date field is raw Entry (acceptable — date_field used elsewhere)
- [-] `_show_biz_edit_dialog` uses raw Entry (acceptable — user enters URLs)
- [-] `_edit_invoice_param` uses raw Entry (acceptable — user enters text)

### 4.2 Performance
- [x] Database indexes added: jobs.status, jobs.customer_id, jobs.due_date, invoices.job_id, invoices.paid, appointments.date, appointments.customer_id
- [-] All filtering is in-memory — acceptable for datasets under ~10,000 records
- [-] Dashboard loads all records — acceptable for small datasets

### 4.3 UI Consistency
- [x] Sidebar dark theme consistent
- [x] Content area scrollable
- [x] Demo mode banner fixed
- [x] Minimum window size enforced
- [x] Window resize doesn't break layout
- [x] Table system consistent across all pages
- [x] Alternating row colors
- [x] No borders (clean look)
- [x] Headers align with columns
- [x] Long text truncates with "..." + tooltip
- [x] Action buttons on far right
- [x] Status badges with colors

### 4.4 Feature Completeness
- [x] Setup wizard with language selection
- [x] PIN login with SHA-256 hash
- [x] License activation with HWID
- [x] Demo mode (7-day, 10-job limit)
- [x] Dashboard with stats, reminders, quick actions
- [x] Jobs: create, list, edit, mark done, search/filter
- [x] Customers: create, list, edit, search/filter
- [x] Appointments: create, list, edit, search/filter
- [x] Invoices: create from job, mark paid, search/filter
- [x] Invoice PDF generation
- [x] Invoice preview with customizable format
- [x] WhatsApp integration
- [x] Email integration
- [x] Google review link
- [x] Reports page with revenue stats
- [x] Backup/restore
- [x] CSV export
- [x] Settings: business info, PIN, language, invoice format, startup, invoice parameters
- [x] Auto-startup
- [x] Language switching (EN/MS/ZH)
- [x] Date picker
- [x] Global search
- [x] Pickup reminders
- [x] Invoice cleanup

---

## 5. BUILD & DISTRIBUTION

- [x] PyInstaller builds successfully
- [x] `.exe` runs on clean Windows install
- [x] All dependencies bundled
- [x] `.gitignore` excludes sensitive files
- [x] No secrets in repository
- [x] Database with test data in `dist/`
- [x] GitHub repo private

---

## 6. TRANSLATION COMPLETENESS

- [x] All UI labels, buttons, headers translated (EN/MS/ZH)
- [x] All error/success messages translated
- [x] All search placeholders translated
- [x] Status badges translated
- [x] Payment method labels translated
- [x] Edit dialog titles translated
- [x] Cleanup messages translated
- [~] WhatsApp/email/PDF templates English-only (acceptable for v1)

---

## 7. KNOWN LIMITATIONS (Acceptable for v1)

1. Customer-facing messages (WhatsApp, email, PDF) are English-only
2. No delete records — prevents accidental loss
3. No undo
4. No customer detail view
5. Address field exists in DB but no UI
6. PIN is not salted
7. License key is weak
8. All filtering is in-memory
9. No migration system

---

*Last updated: 16 August 2026*
