
---

```md
# HRWorks - Employee Time Tracking System 🕒📊

## 🚀 Project Overview
HRWorks is a **Django-based web application** for **employee time tracking**, **vacation management**, and **work hour reporting**. Employees can **clock in & out**, **track overtime**, **view their statistics via interactive charts**, and **export work reports as PDFs**.

---

## 📌 Features Implemented

### **1️⃣ Authentication System**
✔️ **Login & Logout** system with CSRF protection  
✔️ **Admin-Only Registration** – Employees are created by an admin  
✔️ **Role-Based Access Control**:
   - **Admins** manage users & view reports
   - **Employees** track their own work hours

---

### **2️⃣ Employee Dashboard**
✔️ **Compact Time Tracker in Navbar**
   - **Clock In / Clock Out** button (Play/Pause)
   - **Live hours worked today**
   - **Clock-in timestamp** displayed  

✔️ **Work Overview Panel**
   - **Hours Worked Today**
   - **Overtime Calculation**
   - **Vacation Days Remaining**
   - **Monthly Work Hours Overview**

✔️ **Interactive Charts (Chart.js)**
   - **Hours Worked Today (Donut Chart)**
   - **Total Monthly Hours**
   - **Overtime Worked**
   - **Vacation Used**
   - **Vacation Balance**

---

### **3️⃣ Time Management**
✔️ **Employees can clock in & out multiple times daily**  
✔️ **Overtime Calculation**:
   - 8-hour workday cap
   - Extra hours counted as overtime  

✔️ **Vacation Tracking**:
   - Employees have **30 vacation days per year**
   - Taking vacation **reduces balance automatically**  

✔️ **Real-Time Hours Update** – No page refresh needed  

---

### **4️⃣ Role-Based Dashboards**
✔️ **Admins See:**  
   - All employees' hours & reports  
   - Total company overtime stats  

✔️ **Employees See:**  
   - Their own hours & charts  

✔️ **Nav Bar Customization:**  
   - **Admins see additional options**
   - **Employees have limited dashboard features**  

---

### **5️⃣ Export Data as PDF 📄**
✔️ **One-Click PDF Download**  
✔️ **Includes:**
   - Daily Work Hours  
   - Monthly Work Summary  
   - Overtime Details  
   - Vacation Balance  

✔️ **Automatic Formatting** for professional reports  

---

## 📂 Folder Structure
```
hrworks/
│── accounts/                # Django app for time tracking
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Navbar & layout
│   │   ├── dashboard.html   # Employee dashboard
│   │   ├── view_profile.html # Profile management
│   │   ├── edit_profile.html # Edit profile page
│   │   ├── register.html    # Admin user registration
│   │   ├── login.html       # Login page
│   ├── static/              # Static files (CSS, JS, Images)
│── hrworks/                 # Main Django settings
│── media/                   # User-uploaded profile pictures
│── manage.py                # Django management script
```

---

## 🔧 Setup Instructions

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/Bostame/hrworks.git
cd hrworks
```

### **2️⃣ Set Up the Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Apply Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```

### **5️⃣ Create a Superuser**
```sh
python manage.py createsuperuser
```

### **6️⃣ Run the Development Server**
```sh
python manage.py runserver
```

### **7️⃣ Access the Application**
- Open [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)  
- **Admin users** can log in and manage employees  
- **Employees** track their work hours  

---

## 🎯 How to Use

### **Clocking In & Out**
1. **Navigate to the Dashboard**  
2. Click the **Play/Pause** button in the navbar  
3. The system **records your working hours** automatically  

### **Downloading Work Reports**
1. Click **"Download Work Report (PDF)"**  
2. The system **generates a PDF** with work details  

---

## 🚀 Upcoming Enhancements
🔹 **Export Data as CSV**  
🔹 **Automated Email Reports**  
🔹 **Advanced Admin Insights**  
🔹 **Integrations with HR Systems**  

---

## 📜 License
This project is for internal company use only. No public distribution permitted.

---

💡 **Developed by:** Md Bayazid Bostame  
📅 **Last Updated:** March 8, 2025  
```

---
