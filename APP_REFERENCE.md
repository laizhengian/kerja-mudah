# Kerja Mudah - App Reference

This is a complete reference for how the Kerja Mudah app works. Written for humans and AI assistants to understand the full picture without reading code.

---

## What Is This App?

Kerja Mudah is a desktop app for small repair/service shops in Malaysia. It runs offline on Windows as a single .exe file. No internet needed. No cloud. Everything stays on the customer's computer.

**Target businesses:** Phone repair shops, car workshops, electronics repair, any service-based business.

**Languages:** English, Bahasa Malaysia, Chinese (switchable in Settings).

---

## The Big Picture

The app has 8 main sections, accessed from a dark sidebar on the left:

1. **Dashboard** - Overview of everything
2. **Jobs** - Track repair/service jobs
3. **Customers** - Customer database
4. **Appointments** - Schedule appointments
5. **Invoices** - Billing and payments
6. **Reports** - Revenue tracking
7. **Backup** - Save/restore data
8. **Settings** - Business info and preferences

---

## Section by Section

### 1. Dashboard (Home)

The first screen you see. Shows 4 numbers at the top:

- **Active Jobs** - Jobs that are pending or in-progress
- **Appointments** - Appointments scheduled for today
- **Outstanding** - Total unpaid invoice amount
- **Jobs Done (This Month)** - Jobs completed this calendar month

Below the numbers: **Quick Actions** - buttons to quickly create a new Job, Customer, or Appointment.

---

### 2. Jobs

This is the main work area. A job tracks a single repair or service.

**What a job contains:**
- Job code (auto-generated, like JOB-20260815-001)
- Customer (linked from the customer list)
- Item (what's being repaired, e.g. "iPhone 14 Screen")
- Problem (description of the issue)
- Quote (price in RM)
- Status (pending / in-progress / done)
- Due date
- Notes
- Completed date (when marked done)

**How jobs work:**
1. Click "+ New Job" to create one
2. Select an existing customer or create a new one
3. Fill in the item, problem, quote, due date, notes
4. Job appears in the list as "PENDING"
5. Change status to "IN-PROGRESS" when work starts
6. Click "DONE" when finished - this triggers the invoice flow

**When you mark a job as Done**, a popup asks what to do next:
- **Invoice + WhatsApp** - Creates invoice and opens WhatsApp with a message to send to the customer
- **Invoice + Email** - Creates invoice and opens email client
- **Invoice** - Just creates the invoice record
- **Skip** - Marks done without creating invoice

**The table** shows all jobs in a clean grid with columns: Code, Item, Customer, Quote, Status, Due Date, Notes, and action buttons (Done/PDF/Edit). Long text gets cut with "..." and shows full text when you hover over it.

**Search:** Type in the search bar to filter jobs by code, item, customer name, or notes.

---

### 3. Customers

A list of all customers in the system.

**What a customer contains:**
- Name
- Phone number
- Email
- Notes
- Created date

**How customers work:**
1. Click "+ Customer" to add one
2. Fill in name (required), phone, email, notes
3. Customer appears in the list
4. Click "Edit" on any row to change details

**When creating a job**, you pick a customer from this list. If the customer doesn't exist yet, you can create them right from the job form.

**Search:** Type to filter customers by name, phone, or email.

---

### 4. Appointments

Schedule appointments with customers.

**What an appointment contains:**
- Customer (linked from customer list)
- Date
- Time
- Purpose (what the appointment is for)
- Status (scheduled / done)
- Notes

**How appointments work:**
1. Click "+ Appointment" to create one
2. Pick a customer, set date/time/purpose
3. Appointment appears in the list
4. Click "Done" when the appointment is finished
5. Click "Edit" to change details

**Dashboard shows today's appointments** so you know who's coming in.

**Search:** Type to filter appointments by customer name, purpose, or notes.

---

### 5. Invoices

Track payments for completed jobs.

**What an invoice contains:**
- Invoice code (auto-generated, like INV-20260815-001)
- Linked job
- Amount (RM)
- Paid status (unpaid / paid)
- Payment method (Cash / E-Wallet / Card / Transfer)
- Created date

**How invoices work:**
1. An invoice is created when you mark a job as Done (if you chose one of the Invoice options)
2. The invoice starts as UNPAID
3. Send the invoice to the customer via WhatsApp or Email from the Invoices page
4. When the customer pays, click "Pay" and select how they paid (Cash, E-Wallet, Card, or Transfer)
5. Invoice is now marked as PAID

**PDF Invoices:**
- The app can generate professional PDF invoices
- PDFs are saved in the `data/invoices/` folder
- You can download a PDF from the Invoices page or from completed Jobs
- The PDF includes: your business info, customer info, item details, total, payment terms, and thank you note

**Invoice customization** (in Settings):
- Invoice title (e.g., "INVOICE", "RECEIPT", "BILL")
- Payment terms text
- Thank you note
- Footer text
- You can preview how the invoice looks before sending

**Google Review link:** If you added your Google review link in Settings, it's automatically included in WhatsApp and email messages to customers.

**Search:** Type to filter invoices by code, customer name, or amount.

---

### 6. Reports

See how much money the business is making.

**Shows:**
- Today's revenue
- This week's revenue
- This month's revenue
- Total outstanding (unpaid)
- List of recent paid invoices

Big numbers format nicely (e.g., RM 1.2K for RM 1,200, RM 1.5M for RM 1,500,000).

---

### 7. Backup

Protect your data.

**Options:**
- **Backup** - Saves a copy of the database to wherever you choose
- **Restore** - Loads a backup file to replace the current data
- **Export CSV** - Exports customers, jobs, and invoices as spreadsheet files

All data is stored in one SQLite file: `data/data.db`. PDF invoices are in `data/invoices/`.

---

### 8. Settings

Configure the app and business info.

**Business information:**
- Business name
- Phone number
- Email
- Google review link (for sending to customers)

**App preferences:**
- Language (English / Bahasa Malaysia / Chinese)
- Invoice format (Text or PDF)
- Invoice title, payment terms, thank you note, footer
- Open on Windows startup (toggle)
- PIN protection (optional 4-digit code to access Settings)

**Preview:** You can preview how an invoice looks with your current settings before saving.

---

## How the Pieces Connect

```
Customer ──────> Job ──────> Invoice
                  │
                  └────> marked Done triggers invoice creation

Appointment ──> Customer (linked)
```

- A **Job** always belongs to a **Customer**
- An **Invoice** always comes from a **Job**
- An **Appointment** is linked to a **Customer**
- The **Dashboard** pulls numbers from all of these

---

## Special Features

### PIN Protection (Optional)
- Owner can set a 4-digit PIN in Settings
- PIN is required to access Settings (edit business info)
- PIN is stored securely (hashed, not plain text)
- Can be changed or removed anytime
- Has a Show/Hide toggle so you can see what you're typing

### Smart Pickup Reminders
- Tracks jobs that are done but not yet invoiced (meaning customer hasn't paid/picked up)
- Can send WhatsApp reminders to customers to collect their items
- Helps reduce uncollected devices sitting in the shop

### Google Review Integration
- Add your Google review link in Settings
- When you send invoices via WhatsApp or Email, the review link is included automatically
- Customers click the link to leave a Google review
- Builds your online reputation with zero extra effort

### Translation System
- Every word in the app can be shown in English, Malay, or Chinese
- Switch language in Settings
- All three languages are fully translated

### Field Validation
- Every input field has rules to prevent bad data
- Phone numbers only allow digits and +/-
- Email blocks certain special characters
- Dates enforce valid month/day ranges
- PIN only allows 4 digits
- Names block dangerous characters

### Date Format
- All dates display as: "20 Aug 2026" (day month year)

---

## File Structure

```
Kerja Mudah/
    main.py              Everything: UI, logic, translations (one big file)
    database.py          All database operations
    data/
        data.db          The database (auto-created on first run)
        invoices/        PDF invoices saved here
    dist/
        Kerja Mudah.exe  The packaged app
```

The app is two Python files: `main.py` (the app) and `database.py` (the database). Everything else is data.

---

## How It's Built (Simple Version)

- **Language:** Python
- **Look:** Tkinter (Python's built-in drawing tool for windows, buttons, text)
- **Storage:** SQLite (a single file database, like a super-powered Excel)
- **PDFs:** fpdf2 library (creates the PDF invoice files)
- **Packaging:** PyInstaller (turns the Python files into a single .exe)
- **Everything runs offline** - no internet connection needed at any point

---

## How the Tables Look (Jobs Example)

The Jobs table (and all other tables in the app) uses this layout:

| Code | Item | Customer | Quote | Status | Due Date | Notes | Actions |
|------|------|----------|-------|--------|----------|-------|---------|
| JOB-20260815-001 | iPhone 14 Screen | Ahmad | RM 350 | PENDING | 20 Aug 2026 | Cracked display... | Done Edit |

- Headers are at the top in gray text
- Rows alternate between white and light gray backgrounds
- Long text gets cut off with "..." and shows full text when you hover
- Status shows as a colored badge (green for pending, blue for done)
- Action buttons (Done, PDF, Edit) are on the far right

This same pattern is used for Jobs, Customers, Appointments, and Invoices.

---

## What Happens When You Build the .exe

Running this command creates a single .exe file:
```
python -m PyInstaller --onefile --windowed --name "Kerja Mudah" main.py
```

This bundles everything (Python, Tkinter, the database code, PDF library) into one file that runs on any Windows computer without installing anything.

---

## License System

- Each copy of the app is locked to one computer
- The computer has a Hardware ID (HWID)
- A license key is generated from that HWID
- The key is checked when the app starts
- Without a key, the app runs in Demo mode (7 days, max 10 jobs)
- The key generator (`keygen.py`) is only for the seller

---

## Data Safety

- All data is in one file: `data/data.db`
- To fully back up: copy the entire "Kerja Mudah" folder
- To move to a new computer: copy the folder, then reactivate with a new license key
- The app has built-in backup/restore in the Backup section
- CSV export lets you open data in Excel or Google Sheets

---

*Last updated: August 2026*
