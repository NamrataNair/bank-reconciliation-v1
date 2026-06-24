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
* Exception Management
* AI Match Suggestions
* Auto Journal Entries
* Intercompany Reconciliation
* Treasury Management
* Real-Time Bank APIs

## 2. Architecture

**Frontend Layer**
* Technology: Django Templates, HTMX, Bootstrap 5
* Responsibilities: Dashboard, Import screens, Reconciliation screens, Reports, Administration

**Backend Layer**
* Technology: Django, Django REST Framework
* Responsibilities: Authentication, Reconciliation processing, Business rules, Workflow management, Reporting, Integrations

**Processing Layer**
* Technology: Celery, Redis
* Responsibilities: File processing, Matching jobs, Scheduled jobs, Report generation, AI Inference integration

**Database Layer**
* Technology: PostgreSQL (Defaulted to SQLite for local setup)
* Responsibilities: Transaction storage, Audit trail, Workflow state, Reporting

## 3. Functional Modules

**Core Engine**
* Authentication & Security (Users, Roles, Audit)
* Company & Bank Management
* Statement Import (CSV, XLSX, MT940)
* Matching Engine (One-to-One, Many-to-Many, etc.)
* Approval Workflows

**Advanced Modules**
* **Exception Management:** Handles routing and resolution of unmatched or problematic transactions.
* **AI Match Suggestions:** Provides machine-learning based recommendations for potential matches.
* **Auto Journal Entries:** Automatically drafts General Ledger (GL) lines for approved reconciliations.
* **Intercompany Reconciliation:** Reconciles internal transactions between sibling or parent-child companies.
* **Treasury Management:** Tracks projected vs. actual cash positioning across bank accounts.
* **Real-Time Bank APIs:** Integrates directly with banking institutions to pull statement data live.

## 4. Database Design
Core App Tables:
* `users`, `roles`, `permissions`, `audit_logs`, `system_settings`
* `companies`, `branches`
* `banks`, `bank_accounts`

Reconciliation App Tables:
* `import_batches`
* `bank_transactions`, `source_transactions`
* `reconciliation_groups`, `reconciliation_items`
* `approval_workflows`, `approval_actions`

Advanced Phase App Tables:
* `ExceptionCase` (exception_management)
* `MatchSuggestion` (ai_matching)
* `JournalEntry`, `JournalEntryLine` (journal_entries)
* `IntercompanyTransaction` (intercompany)
* `TreasuryPosition` (treasury)
* `BankAPIConnection` (realtime_banks)

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

#### Method 1: Local Development (SQLite)

To run the full stack locally without Docker, you need to run three separate processes. It is recommended to open three terminal windows.

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

#### Method 2: Deployment via Docker Compose

To deploy the entire platform including PostgreSQL, Redis, Celery, Gunicorn, and Nginx using Docker:

1. Ensure Docker and Docker Compose are installed.
2. Build and start the services in the background:
   ```
   docker-compose up -d --build
   ```

Once all containers are up and running, you can access the platform at:
- Web Interface: [http://localhost/](http://localhost/)
- API Endpoints: [http://localhost/api/](http://localhost/api/)
- Django Admin: [http://localhost/admin/](http://localhost/admin/)

---

## Testing

To run the unit test suite across the core, api, and advanced applications, execute:
```
python manage.py test
```

---

## Future Roadmap
* ML Matching Engine (Implementation & Tuning)
* Predictive Reconciliation
* Advanced Analytics Dashboards
