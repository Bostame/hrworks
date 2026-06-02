# HRWorks - Employee Time Tracking System 🕒📊

HRWorks is a Django-based employee management web application designed for time tracking, vacation management, overtime calculation, and work-hour reporting.

Employees can clock in and out, track their daily and monthly working hours, view overtime and vacation balances, and export professional work reports as PDF files.

---

## 🚀 Project Overview

HRWorks helps companies manage employee working hours in a structured and user-friendly way.

The system includes:

* Employee clock-in and clock-out tracking
* Multiple work sessions per day
* Daily and monthly work-hour summaries
* Overtime calculation
* Vacation balance tracking
* Role-based dashboards for admins and employees
* PDF work report generation
* Interactive dashboard charts using Chart.js

---

## 📌 Features Implemented

### 1. Authentication System

* Login and logout system with CSRF protection
* Admin-only employee registration
* Role-based access control

#### User Roles

| Role     | Permissions                                                         |
| -------- | ------------------------------------------------------------------- |
| Admin    | Manage users, view employee reports, access company-wide statistics |
| Employee | Track personal work hours, view own dashboard, download own reports |

---

### 2. Employee Dashboard

The employee dashboard provides a clear overview of the current workday, monthly statistics, vacation information, and overtime balance.

#### Dashboard Features

* Compact time tracker in the navbar
* Clock In / Clock Out button
* Live hours worked today
* Clock-in timestamp display
* Work overview panel
* Monthly work-hour overview
* Vacation balance overview
* Overtime tracking

---

### 3. Interactive Charts

HRWorks uses Chart.js to display employee statistics in a visual and easy-to-understand format.

Implemented charts include:

* Hours worked today
* Total monthly hours
* Overtime worked
* Vacation used
* Vacation balance

---

### 4. Time Management

Employees can track their working hours directly from the dashboard.

#### Supported Time Tracking Features

* Clock in and clock out
* Multiple clock-ins and clock-outs per day
* Automatic daily work-hour calculation
* Real-time hours update without page refresh
* 8-hour standard workday calculation
* Automatic overtime calculation after 8 hours

---

### 5. Vacation Tracking

HRWorks includes a basic vacation management system.

#### Vacation Rules

* Each employee starts with 30 vacation days per year
* Approved vacation days reduce the remaining balance automatically
* Employees can view their remaining vacation balance from the dashboard

---

### 6. Role-Based Dashboards

The system provides different dashboard views depending on the user role.

#### Admin Dashboard

Admins can view:

* All employee work-hour reports
* Employee overtime statistics
* Company-wide work summaries
* User management options

#### Employee Dashboard

Employees can view:

* Their own work hours
* Their own overtime
* Their own vacation balance
* Their own PDF reports

---

### 7. PDF Work Reports 📄

Employees and admins can export work-hour data as PDF reports.

#### PDF Report Includes

* Daily work hours
* Monthly work summary
* Overtime details
* Vacation balance
* Professionally formatted report layout

---

## 📂 Folder Structure

```text
hrworks/
│
├── accounts/                    # Django app for authentication and time tracking
│   ├── migrations/              # Database migrations
│   ├── templates/               # HTML templates
│   │   ├── base.html            # Main layout and navbar
│   │   ├── dashboard.html       # Employee dashboard
│   │   ├── view_profile.html    # Profile view page
│   │   ├── edit_profile.html    # Profile edit page
│   │   ├── register.html        # Admin-only user registration
│   │   └── login.html           # Login page
│   │
│   └── static/                  # CSS, JavaScript, and image files
│
├── hrworks/                     # Main Django project settings
├── media/                       # Uploaded user profile pictures
├── manage.py                    # Django management script
└── requirements.txt             # Python dependencies
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Bostame/hrworks.git
cd hrworks
```

### 2. Create and Activate a Virtual Environment

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Open the Application

Visit the application in your browser:

```text
http://127.0.0.1:8000/login/
```

---

## 🎯 How to Use

### Admin Usage

1. Log in with an admin account.
2. Register employees from the admin-only registration page.
3. View employee work-hour reports.
4. Monitor overtime and vacation balances.

### Employee Usage

1. Log in with an employee account.
2. Open the dashboard.
3. Click the Clock In button to start working.
4. Click the Clock Out button when finished.
5. View daily and monthly work-hour statistics.
6. Download PDF work reports when needed.

---

## 📄 Downloading Work Reports

To download a PDF work report:

1. Go to the dashboard.
2. Click **Download Work Report (PDF)**.
3. The system generates a professional PDF report containing work-hour and vacation details.

---

## 🛠️ Technologies Used

* Python
* Django
* HTML
* CSS
* JavaScript
* Bootstrap
* Chart.js
* SQLite / Django ORM
* PDF generation tools

---

## 🚀 Upcoming Enhancements

Planned future improvements include:

* CSV export
* Automated email reports
* Advanced admin analytics
* HR system integrations
* Leave request approval workflow
* Improved monthly reporting
* Calendar-based vacation overview

---

## 📜 License

This project is licensed under the MIT License.

You are free to use, modify, distribute, and sublicense this project under the terms of the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Developed by:** Md Bayazid Bostame
**Last Updated:** March 8, 2025
