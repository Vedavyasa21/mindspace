# 🧠 MindSpace – Student Mental Health & Wellness Platform

A Django full-stack web application for student mental health support.

## 🚀 Quick Start

### Step 1: Install Requirements
```bash
pip install django pillow
```

### Step 2: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser (optional, one already seeded)
```bash
python manage.py createsuperuser
```

### Step 4: Run Server
```bash
python manage.py runserver
```

### Step 5: Open Browser
Go to: http://127.0.0.1:8000

---

## 🔐 Demo Login Credentials

| Role      | Username   | Password      |
|-----------|------------|---------------|
| Admin     | admin      | admin123      |
| Counselor | dr_sarah   | counselor123  |
| Counselor | dr_raj     | counselor123  |
| Student   | student1   | student123    |

---

## 📁 Project Structure
```
mindspace/
├── accounts/         # Auth, roles, profiles
├── wellness/         # Resources, dashboards
├── counseling/       # Session booking
├── anonymous_support/ # Anonymous posts
├── templates/        # All HTML templates
└── manage.py
```

## 🛠 Tech Stack
- Python 3.x + Django
- Bootstrap 5 + Font Awesome
- SQLite (development)

## 👥 Roles
- **Admin** – Manages platform, users, resources
- **Student** – Books sessions, browses resources, posts anonymously
- **Counselor** – Responds to sessions and anonymous posts
