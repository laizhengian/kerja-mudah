# Kerja Mudah - Audit Checklist

Complete checklist for verifying the app is production-ready.

## Status Legend
- [ ] Not started
- [~] In progress
- [x] Completed

---

## 1. UI/UX - Visual Quality

### Table System (All Pages)
- [x] Jobs table uses grid layout with cell() helper
- [x] Customers table uses grid layout with cell() helper
- [x] Appointments table uses grid layout with cell() helper
- [x] Invoices table uses grid layout with cell() helper
- [x] All tables have alternating row colors (white/light gray)
- [x] No borders on table rows (clean look)
- [x] Headers align with data columns
- [x] Long text truncates with "..." and shows full text on hover
- [x] Action buttons always visible on far right
- [x] Status badges (PENDING/DONE) with colored backgrounds
- [x] Due dates show full format (20 Aug 2026)

### Layout
- [x] Sidebar dark theme with business name
- [x] Content area scrollable
- [x] Demo mode banner fixed at top
- [x] Minimum window size enforced (900x650)
- [x] Window resize doesn't break layout
- [x] Quick Actions on dashboard

### Typography
- [x] Font sizes consistent (Segoe UI 11 for data, 10 for headers)
- [x] Bold for important fields (names, codes, quotes)
- [x] Gray for secondary text (dates, notes)
- [x] Status badges readable on colored backgrounds

### Colors
- [x] Green for success/done/paid
- [x] Orange for warnings/pending
- [x] Red for errors/unpaid
- [x] Blue for in-progress/info
- [x] Purple for PDF buttons
- [x] Consistent color scheme across all pages

---

## 2. Input Validation

### Field Limits
- [x] Name fields: blocked `<>{}[]|\"'`, max 50 chars
- [x] Phone fields: digits + `+-` only, max 20 chars
- [x] Email fields: blocked `<>{}[]|\`, max 80 chars
- [x] PIN field: 4 digits only, displays as `*`
- [x] Number fields: digits + `.-` only, max 12 chars
- [x] Date fields: month 1-12, day 1-31 enforced
- [x] Search fields: max 80 chars
- [x] General text fields: max 80 chars

### Required Fields
- [x] Customer name required for new jobs
- [x] Item required for new jobs
- [x] Date required for new appointments

---

## 3. Data Handling

### Database
- [x] All queries use parameterized statements (no SQL injection)
- [x] Foreign key relationships maintained
- [x] Backup/restore works correctly
- [x] CSV export produces valid files

### File Operations
- [x] PDF generation handles all edge cases
- [x] File paths handle spaces and special characters
- [x] Error handling on all file operations

---

## 4. Error Handling

### Crash Prevention
- [x] All database writes wrapped in try/except
- [x] All file operations wrapped in try/except
- [x] All webbrowser.open wrapped in try/except
- [x] All os.startfile wrapped in try/except

### User-Facing Errors
- [x] Clear error messages (no raw Python exceptions)
- [x] Confirmation dialogs for destructive actions
- [x] Success messages after operations

---

## 5. Feature Completeness

### Core Features
- [x] Job creation, editing, status changes
- [x] Customer creation, editing
- [x] Appointment creation, editing
- [x] Invoice creation from jobs
- [x] Invoice payment marking
- [x] PDF invoice generation

### Integrations
- [x] WhatsApp links open correctly
- [x] Email mailto links work
- [x] Google review links convert correctly
- [x] CSV export produces valid files

### Search
- [x] Jobs search filters by code, item, customer, notes
- [x] Customers search filters by name, phone, email
- [x] Appointments search filters by customer, purpose, notes
- [x] Invoices search filters by code, customer
- [x] Search trace race conditions fixed (trace after frame creation)

---

## 6. Translation

- [x] All UI strings use self.t("key")
- [x] No hardcoded English in UI
- [x] All 3 languages have identical key sets
- [x] Malay and Chinese translations are natural

---

## 7. Security

- [x] PIN stored as SHA-256 hash (not plaintext)
- [x] License key validation is cryptographically sound
- [x] No secrets in source code
- [x] No sensitive data in error messages

---

## 8. Build & Distribution

- [x] PyInstaller builds successfully
- [x] .exe runs on clean Windows install
- [x] All dependencies bundled
- [x] .gitignore excludes sensitive files (keygen.py, SALES_CHEAT_SHEET.txt, data/, dist/, build/, *.spec, *.db)
- [x] No secrets in repository

---

*Last updated: August 2026*
