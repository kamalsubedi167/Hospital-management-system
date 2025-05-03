Hospital Management System (HMS) Documentation
Overview
The Hospital Management System (HMS) is a web-based application developed using Django to manage patient records, appointments, lab reports, and billing efficiently. It supports both administrative and doctor roles with a secure and user-friendly interface.
Installation

Prerequisites:
Python 3.13 or later
Git
pip (Python package manager)


Clone the Repository:git clone "paxi rakhumla ni "
cd hms_project


Set Up Virtual Environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:pip install -r requirements.txt


Configure Database:
Update settings.py with your database credentials (default is SQLite).


Apply Migrations:python manage.py migrate


Run the Server:python manage.py runserver



Key Features

Patient Management: Add, edit, delete, and filter patients by doctor, gender, and blood group.
Appointment Scheduling: Schedule, filter, and export appointments by date and status.
Lab Reports: Manage and filter lab reports by test name and date.
Billing: Track and manage patient billing.
User Roles: Separate permissions for admins and doctors.

Usage

Admin: Can perform all actions including adding users, managing inventory, and exporting data.
Doctor: Can view assigned patients, appointments, and pending lab reports.

Future Improvements

User feedback integration.
Enhanced reporting features.

Technical Details

Framework: Django (MVT architecture)
Database: SQLite (default), configurable to PostgreSQL
Dependencies: django-ratelimit, others listed in requirements.txt

