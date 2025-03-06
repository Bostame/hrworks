Here's a **README.md** file summarizing everything we have done so far in your Django project:  

---

```md
# HRWorks - Django Web Application

## 🚀 Project Overview
HRWorks is a Django-based web application for managing employee data, user authentication, and role-based access. The project includes user registration, profile management, dashboard views, and Bootstrap-enhanced UI.

---

## 📌 Features Implemented

### **1. Authentication System**
- ✅ **Login System** with a user-friendly interface.
- ✅ **Logout Functionality** with CSRF protection.
- ✅ **Role-based Access**:
  - Admins can add new users.
  - Regular users can only view and edit their own data.

### **2. User Dashboard**
- ✅ **Dashboard with Navbar**:
  - Company logo (left).
  - Profile dropdown (right) with:
    - View Profile Data
    - Add New User (Admins only)
    - Logout
- ✅ **Personalized Welcome Message**.

### **3. User Profile Management**
- ✅ **View Profile Page**:
  - Displays all user data in a structured format.
  - Includes employment, contact, and wage details.
- ✅ **Edit Profile Page**:
  - Allows users to update their information.
  - Success message displayed upon saving.
- ✅ **Profile Picture Upload**:
  - Users can upload profile pictures.
  - Defaults to `default_profile.png` if none is provided.

### **4. User Registration**
- ✅ **Admin-Only User Creation**:
  - Admins can register new users.
  - Form structured with Bootstrap styling.
- ✅ **Includes Fields**:
  - Personal details (Name, DOB, Citizenship, etc.).
  - Contact details (Email, Phone, Emergency Contact).
  - Employment details (Position, Start Date, etc.).
  - Wage data (Tax ID, Child Allowance, etc.).
  - Password fields.

### **5. Enhanced UI with Bootstrap**
- ✅ **Consistent Navbar on All Pages**:
  - Hidden profile dropdown when user is not logged in.
  - Clicking the company logo redirects to:
    - Dashboard (if logged in).
    - Login page (if not authenticated).
- ✅ **Login Page Redesign**:
  - Centered form with Bootstrap styling.
  - Welcome message and logo at the top.
  - Improved form fields with placeholders.

### **6. Profile Picture Handling**
- ✅ **Custom Profile Picture Support**:
  - Users can upload profile pictures.
  - Displays uploaded picture in the navbar.
  - Defaults to a placeholder image if none is uploaded.

---

## 📂 Folder Structure
```
hrworks/
│── accounts/                # Django app for user management
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template (Navbar, Layout)
│   │   ├── dashboard.html   # User dashboard
│   │   ├── view_data.html   # View user data page
│   │   ├── edit_profile.html # Edit user profile page
│   │   ├── register.html    # Admin user registration page
│   │   ├── login.html       # Login page
│   ├── static/              # Static files (CSS, JS, Images)
│── hrworks/                 # Main Django project settings
│── media/                   # User-uploaded profile pictures
│── manage.py                # Django management script
```

---

## 🔧 Setup Instructions
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/Bostame/hrworks.git
   cd hrworks
   ```

2. **Create & Activate Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```sh
   python manage.py runserver
   ```

6. **Access the Application**:
   - Open [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/) to log in.

---

## 🔧 Upcoming Enhancements
🔹 **Forgot Password Feature**  
🔹 **User Role Management**  
🔹 **Dynamic Dashboard Widgets**  
🔹 **Better Styling & Responsiveness**  

---

## 📜 License
This project is for internal use. No public distribution permitted.

---

💡 **Developed by:** Md Bayazid Bostame  
📅 **Last Updated:** March 6, 2025  
```

---

This **README.md** file gives a structured overview of the project, covering all the features you have implemented so far. It also includes **setup instructions**, **folder structure**, and **next steps**. 🚀
