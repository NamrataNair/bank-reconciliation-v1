# Bank Reconciliation Platform

## 1. Objective
Develop a configurable bank reconciliation platform capable of reconciling:
* Bank statements
* UPI transactions
* NEFT/RTGS/IMPS transactions
* Debit card transactions
* Credit card transactions
* Payment gateway settlements
* Payroll payments
* Vendor payments
* Customer receipts
* Bank interest
* TDS deductions
* Bank charges

The platform supports:
* Automated matching
* Manual reconciliation
* Approval workflows
* Audit trails
* Multi-company support
* Multi-bank support
* Multi-currency support

## 2. Architecture

**Frontend Layer**
* Technology: Django Templates, HTMX, Bootstrap 5
* Responsibilities: Dashboard, Import screens, Reconciliation screens, Reports, Administration

**Backend Layer**
* Technology: Django, Django REST Framework
* Responsibilities: Authentication, Reconciliation processing, Business rules, Workflow management, Reporting

**Processing Layer**
* Technology: Celery, Redis
* Responsibilities: File processing, Matching jobs, Scheduled jobs, Report generation

**Database Layer**
* Technology: PostgreSQL (Defaulted to SQLite for local setup)
* Responsibilities: Transaction storage, Audit trail, Workflow state, Reporting

## 3. Functional Modules

**Authentication & Security**
* Features: Login, Logout, Password reset, Session management
* Roles: Administrator, Reconciliation User, Reviewer, Approver, Auditor

**Company Management**
* Manage: Companies, Branches, Departments
* Fields: Company Code, Company Name, GST Number, PAN Number, Currency

**Bank Management**
* Manage: Banks, Bank Accounts
* Fields: Account Number, Account Type, Currency, Opening Balance

**Statement Import**
* Supported Formats: CSV, XLSX, MT940
* Validation: Duplicate file detection, Mandatory field validation, Format validation
* Process: Upload -> Validation -> Staging -> Transaction Creation -> Audit Logging

**Transaction Repository**
* Store all normalized transactions from sources like BANK, UPI, CARD, PAYROLL, AP, AR, TAX, GATEWAY.

**Matching Engine**
* Supported Matching: One-to-One, One-to-Many, Many-to-One, Many-to-Many
* Matching Criteria: Reference Number, UTR, RRN, Amount, Date, Settlement ID

**UPI & Gateway Reconciliation**
* Captures IDs, Amounts, Fees, GST, and Net Settlement with automated matching rules.

**Approval Workflow**
* States: Draft -> Prepared -> Reviewed -> Approved
* Actions: Approve, Reject, Send Back

**Audit Trail**
* Tracks all activities with immutable records.

## 4. Database Design
Core Tables:
* `users`, `roles`, `permissions`
* `companies`, `branches`
* `banks`, `bank_accounts`
* `import_batches`
* `bank_transactions`, `source_transactions`
* `reconciliation_groups`, `reconciliation_items`
* `approval_workflows`, `approval_actions`
* `tds_entries`, `interest_entries`
* `audit_logs`, `report_requests`, `system_settings`

---

## 5. Getting Started

### Prerequisites

Ensure you have the following installed on your local machine:
- Python (>= 3.10)
- Redis Server (Required for Celery background tasks)
- Git

### Installation Steps

1. **Clone the repository:**
   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create and activate a virtual environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```
   python manage.py migrate
   ```

5. **(Optional) Create a superuser account for administration:**
   ```
   python manage.py createsuperuser
   ```

### Execution Steps

To run the full stack locally, you need to run three separate processes. It is recommended to open three terminal windows.

**Terminal 1: Start the Redis Server**
Make sure the Redis server is running. If you are on Linux or macOS, you can typically start it using:
```
redis-server
```

**Terminal 2: Start the Celery Worker**
Activate your virtual environment and start the Celery worker to handle background reconciliation jobs:
```
celery -A bank_reconciliation worker -l info
```

**Terminal 3: Start the Django Development Server**
Activate your virtual environment and start the web server:
```
python manage.py runserver
```

Once running, you can access the platform at:
- Web Interface: [http://localhost:8000/](http://localhost:8000/)
- API Endpoints: [http://localhost:8000/api/](http://localhost:8000/api/)
- Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Testing

To run the unit test suite across the core, api, and reconciliation applications, execute:
```
python manage.py test
```

---

## Future Roadmap
* Phase 2: Exception Management, AI Match Suggestions, Auto Journal Entries
* Phase 3: Intercompany Reconciliation, Treasury Management, Advanced Analytics
* Phase 4: ML Matching Engine, Predictive Reconciliation, Real-Time Bank APIs
