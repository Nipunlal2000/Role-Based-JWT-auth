# 🛡️ Django User Role Management System

A Django REST Framework-based user management system with custom user roles, OTP-based email verification, and permission-based access control for views. Built with scalability, security, and clarity in mind.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-API-red.svg)](https://www.django-rest-framework.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)]()
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)]()

## 🚀 Features

- ✅ Custom User Model (`Profile`) with roles: `SuperAdmin`, `Admin`, `Manager`, `Member`
- 🔐 JWT Authentication using `SimpleJWT`
- 📨 OTP Email Verification (on registration)
- 🔒 Role-based Permissions (Custom permission classes)
- 👤 Profile Creation for each Role
- 🛠️ SuperAdmin User Management (View/Filter/Search/Update/Delete users)
- 🔎 Role, Email, and `is_active` Filtering with Django Filter
- 🔍 Search Users by Email
- 📬 Email backend ready for OTP delivery

---

## 🏗️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** JWT (via `SimpleJWT`)
- **Permissions:** Custom DRF permission classes
- **Filtering:** `django-filter`

---

## 📁 Project Structure (Highlights)

project/ <br>
├── accounts/ # Custom user and role logic <br>
│ ├── models.py # Custom user model & role-specific models <br>
│ ├── serializers.py # Role-specific & login/register serializers <br>
│ ├── views.py # Auth, user detail, and management views <br>
│ ├── permissions.py # Role-based custom permission classes <br>
│ ├── utils.py # OTP generation & email sending <br>
│ <br>
├── urls.py # Root URL configuration <br> 
├── settings.py # Installed apps, JWT config, etc. <br>

## 🔐 Permission Login

| Role       | Can View Member | Can View Manager | Can View Admin | Can View SuperAdmin |
| ---------- | --------------- | ---------------- | -------------- | ------------------- |
| Member     | ✅ Self only     | ❌                | ❌              | ❌                   |
| Manager    | ✅ All Members   | ✅ Self           | ❌              | ❌                   |
| Admin      | ✅ All Members   | ✅ All Managers   | ✅ Self         | ❌                   |
| SuperAdmin | ✅ Everyone      | ✅ Everyone       | ✅ Everyone     | ✅ Self              |

## 🔑 API Endpoints

| Endpoint                  | Method    | Description                          |
| ------------------------- | --------- | ------------------------------------ |
| `/register/`              | POST      | Register a new user and send OTP     |
| `/verify-otp/`            | POST      | Verify OTP and activate user         |
| `/login/`                 | POST      | Login and receive JWT tokens         |
| `/member/me/`             | GET/PATCH | Member access to their own profile   |
| `/members/<id>/`          | GET/PATCH | Admin/Manager/SuperAdmin access      |
| `/superadmin/users/`      | GET       | SuperAdmin fetch/filter/search users |
| `/superadmin/users/<id>/` | DELETE    | SuperAdmin delete user               |


### Configure .env

SECRET_KEY=your_secret_key <br>
EMAIL_HOST_USER=your_email@example.com <br>
EMAIL_HOST_PASSWORD=your_email_password       # GOOGLE PASSKEY generated password not gmail password

## 📬 Email OTP Setup

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' <br>
EMAIL_HOST = 'smtp.gmail.com' <br>
EMAIL_PORT = 587 <br>
EMAIL_USE_TLS = True <br>
EMAIL_HOST_USER = 'your_email@gmail.com' <br>
EMAIL_HOST_PASSWORD = 'your_email_password'


