# Bank Reconciliation Platform

## Overview
A configurable bank reconciliation platform capable of reconciling various financial statements and transactions such as Bank statements, UPI, NEFT/RTGS/IMPS, debit/credit cards, payment gateway settlements, payroll, vendors, customer receipts, interest, TDS, and bank charges.

The platform supports automated matching, manual reconciliation, approval workflows, audit trails, and multi-company/bank/currency support.

## Architecture

### Frontend Layer
- **Technology:** Django Templates, HTMX, Bootstrap 5
- **Responsibilities:** Dashboard, Import screens, Reconciliation screens, Reports, Administration

### Backend Layer
- **Technology:** Django, Django REST Framework
- **Responsibilities:** Authentication, Reconciliation processing, Business rules, Workflow management, Reporting

### Processing Layer
- **Technology:** Celery, Redis
- **Responsibilities:** File processing, Matching jobs, Scheduled jobs, Report generation

### Database Layer
- **Technology:** PostgreSQL
- **Responsibilities:** Transaction storage, Audit trail, Workflow state, Reporting

## Setup & Deployment (Docker)

This platform is configured to be deployed using Docker, Gunicorn, Nginx, Redis, and Celery Workers.

1. Configure environment variables in an `.env` file for Postgres and Redis.
2. Build and run using Docker Compose:
   ```bash
   docker-compose up -d --build
   ```
3. Run migrations and create superuser:
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

## Development Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure Redis and PostgreSQL are running.
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run Celery Worker:
   ```bash
   celery -A bank_reconciliation worker -l info
   ```
5. Run Django Server:
   ```bash
   python manage.py runserver
   ```
