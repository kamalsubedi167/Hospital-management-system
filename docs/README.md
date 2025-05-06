Hospital Management System (HMS) Documentation
Overview
The Hospital Management System (HMS) is a web-based application developed using Django to manage patient records, appointments, lab reports, billing, and feedback efficiently. It supports both administrative and doctor roles with a secure, user-friendly, and responsive interface.
Installation

Prerequisites:

Python 3.13 or later
Git
pip (Python package manager)


Clone the Repository:
git clone https://github.com/your-username/hms_project.git
cd hms_project


Set Up Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Configure Database:

Update settings.py with your database credentials (default is SQLite).


Apply Migrations:
python manage.py migrate


Run the Server:
python manage.py runserver



Key Features

Patient Management: Add, edit, delete, and filter patients by doctor, gender, and blood group.
Appointment Scheduling: Schedule, filter, and export appointments by date and status.
Lab Reports: Manage and filter lab reports by test name and date, with support for file uploads (images, PDFs, videos, X-rays).
Billing: Track and manage patient billing.
User Roles: Separate permissions for admins and doctors.
Feedback System: Submit and manage feedback for system improvements.
Data Export: Export patient and appointment data as CSV files.
Responsive UI: Fully responsive design with a toggleable sidebar for mobile devices.

Usage
Admin User

Login: Access the system with admin credentials.
Dashboard: View statistics like total patients, appointments, and pending lab reports.
Screenshot: [Insert Dashboard Screenshot]


Patient Management:
Add new patients, edit existing ones, or delete records.
Filter by doctor, gender, or blood group.
Export patient list as CSV.
Screenshot: [Insert Patient List Screenshot]


Appointments:
Schedule new appointments, edit, or delete existing ones.
Filter by date range, status, or associated doctor/patient.
Export appointments as CSV.
Screenshot: [Insert Appointment List Screenshot]


Lab Reports:
Add or update lab reports with file uploads (e.g., X-rays, PDFs).
Filter by test name, date, or status.
Screenshot: [Insert Lab Report List Screenshot]


Feedback:
View all feedback submissions and mark them as resolved.
Screenshot: [Insert Feedback List Screenshot]



Doctor User

Login: Access the system with doctor credentials.
Dashboard: View assigned patients, upcoming appointments, and pending lab reports.
Patients: View and manage assigned patients.
Appointments: View and manage appointments associated with the doctor.
Lab Reports: View and update lab reports for assigned patients.
Feedback: Submit feedback or view personal submissions.

Technical Details

Framework: Django (Model-View-Template architecture)
Database: SQLite (default), configurable to PostgreSQL
Dependencies:
django-ratelimit for login rate limiting
chart.js for dashboard visualizations
Others listed in requirements.txt


Models:
Patient: Stores patient details (ID, name, DOB, gender, etc.).
Doctor: Stores doctor profiles linked to users.
Appointment: Manages appointment schedules.
LabReport: Stores lab reports with file uploads.
Feedback: Stores user feedback submissions.


Security:
Input validation for forms.
CSRF protection and XSS prevention.
Rate limiting on login attempts.



Future Improvements

Advanced Reporting: Generate PDF reports for patient history.
Email Notifications: Send appointment reminders via email.
Audit Logs: Track user actions for accountability.
Deployment: Deploy to a production server with PostgreSQL.

Troubleshooting

File Upload Issues: Ensure MEDIA_ROOT and MEDIA_URL are configured in settings.py, and the media/ directory is writable.
Permission Errors: Verify user group assignments (Admin/Doctor) in the Django admin panel.
Responsive Design: Test on multiple devices to ensure the sidebar toggle works correctly.

