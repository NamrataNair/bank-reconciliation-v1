# Bank Reconciliation Platform - Complete Design Document (V1)

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

The platform should support:
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
* Technology: PostgreSQL
* Responsibilities: Transaction storage, Audit trail, Workflow state, Reporting

## 3. Functional Modules

### Authentication & Security
**Features:**
* Login
* Logout
* Password reset
* Session management

**Roles:**
* Administrator
* Reconciliation User
* Reviewer
* Approver
* Auditor

### Company Management
**Manage:**
* Companies
* Branches
* Departments

**Fields:**
* Company Code
* Company Name
* GST Number
* PAN Number
* Currency

### Bank Management
**Manage:**
* Banks
* Bank Accounts

**Fields:**
* Account Number
* Account Type
* Currency
* Opening Balance

### Statement Import
**Supported Formats:**
* CSV
* XLSX
* MT940

**Validation:**
* Duplicate file detection
* Mandatory field validation
* Format validation

**Process:**
Upload → Validation → Staging → Transaction Creation → Audit Logging

### Transaction Repository
Store all normalized transactions.
**Sources:**
* BANK
* UPI
* CARD
* PAYROLL
* AP
* AR
* TAX
* GATEWAY

### Matching Engine
**Supported Matching:**
* One-to-One: Invoice ↔ Receipt
* One-to-Many: Single Bank Entry ↔ Multiple Ledger Entries
* Many-to-One: Multiple Receipts ↔ Single Settlement
* Many-to-Many: Settlement Group ↔ Ledger Group

**Matching Criteria:**
* Reference Number
* UTR
* RRN
* Amount
* Date
* Settlement ID

### UPI Reconciliation
**Capture:**
* UPI ID
* RRN
* Payer Name
* Amount

**Matching Rules:**
* Exact RRN
* Amount
* Date

### Gateway Reconciliation
**Supported:**
* Razorpay
* Cashfree
* Stripe
* PayU

**Components:**
* Gross Amount
* Gateway Fee
* GST
* Net Settlement

### Payroll Reconciliation
**Support:**
* Salary Batch
* Salary Payment File
* Bank Debit Matching

### Vendor Payment Reconciliation
**Support:**
* Bulk Vendor Payments
* NEFT Runs
* RTGS Payments

### Interest Reconciliation
**Support:**
* Savings Interest
* FD Interest

**Entries:**
Bank Dr To Interest Income

### TDS Reconciliation
**Support:**
* TDS on Interest
* Customer TDS

**Entries:**
Bank Dr, TDS Receivable Dr To Income

### GST Support
**Support GST on:**
* Gateway Charges
* Bank Charges

### Approval Workflow
**States:**
Draft, Prepared, Reviewed, Approved

**Actions:**
Approve, Reject, Send Back

### Audit Trail
**Track:**
* Login
* Imports
* Matches
* Reversals
* Approvals
* Configuration Changes

Audit records must be immutable.

## 4. Database Design
**Core Tables:**
* `users`, `roles`, `permissions`
* `companies`, `branches`
* `banks`, `bank_accounts`
* `import_batches`
* `bank_transactions`
* `source_transactions`
* `reconciliation_groups`
* `reconciliation_items`
* `approval_workflows`
* `approval_actions`
* `tds_entries`
* `interest_entries`
* `audit_logs`
* `report_requests`
* `system_settings`

## 5. Frontend Screens
**Dashboard:**
Widgets: Total Transactions, Matched Transactions, Pending Transactions, Match %, Imports Today

**Company Maintenance:**
Create/Edit/Delete Company

**Bank Account Maintenance:**
Create/Edit/Delete Bank Accounts

**Statement Upload:**
Upload File, View Import Status, Import History

**Transaction Browser:**
Filters: Date, Bank, Amount, Status, Source
Actions: View, Export

**Auto Match Screen:**
Run Matching, View Results, Approve Matches

**Manual Match Screen:**
Left Grid: Bank Transactions
Right Grid: Source Transactions
Actions: Match, Split, Merge, Unmatch

**Approval Queue:**
Pending Approvals, Review, Approve, Reject

**Reports:**
Bank Reconciliation Statement, Interest Report, TDS Report, Charges Report, Pending Reconciliation Report

## 6. REST APIs
* Authentication APIs
* Company APIs
* Bank APIs
* Import APIs
* Transaction APIs
* Matching APIs
* Approval APIs
* Report APIs
* Audit APIs

## 7. Security
* Password Policy
* Role Based Access Control
* Session Timeout
* Audit Logging
* CSRF Protection
* Input Validation
* Encryption of Sensitive Data

## 8. Background Jobs
* Import Job
* Auto Matching Job
* Report Generation Job
* Cleanup Job
* Notification Job

## 9. Performance Targets
* Import: 50,000 records under 2 minutes
* Matching: 100,000 transactions under 5 minutes
* Concurrent Users: 100+
* Database: Millions of transaction records

## 10. Deployment
* Docker
* Nginx
* Gunicorn
* Redis
* Celery Workers
* PostgreSQL
* Linux Server

## 11. Future Roadmap

**Phase 2:**
* Exception Management
* AI Match Suggestions
* Auto Journal Entries

**Phase 3:**
* Intercompany Reconciliation
* Treasury Management
* Advanced Analytics

**Phase 4:**
* ML Matching Engine
* Predictive Reconciliation
* Real-Time Bank APIs

---

## Getting Started

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

To run the unit test suite across the core, api, and advanced applications, execute:
```
python manage.py test
```
