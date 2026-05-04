# 🍎 Fitzy – Fitness & Nutrition Tracking Web Application

## 📌 Overview

Fitzy is a Django-based web application designed to help users monitor their daily nutrition and essential health metrics. It provides tools to calculate calorie needs, protein intake, and Body Mass Index (BMI), along with features to track and store personal health data securely.

---

## 🎯 Objective

The goal of Fitzy is to provide a simple and efficient platform for users to:

* Calculate daily calorie requirements
* Calculate protein intake requirements
* Calculate BMI (Body Mass Index)
* Track daily nutrition consumption
* Store and manage personal health data

---

## 🚀 Key Features

* 🔐 User Authentication (Login & Signup)
* 🔥 Calorie Requirement Calculator
* 💪 Protein Requirement Calculator
* ⚖️ BMI Calculator
* 📊 Daily Nutrition Tracking (for logged-in users)
* 🗂️ Food Database with nutritional values
* 🔒 Secure data storage using Django Authentication
* 🎨 Simple and user-friendly interface

---

## 👥 User Roles

### 🔓 Unauthenticated Users

Users who are not logged in can:

* Calculate calorie requirements
* Calculate protein requirements
* Calculate BMI

> ⚠️ Note: They cannot save or track their data.

---

### 🔐 Authenticated Users

Logged-in users get access to advanced features:

* Enter personal details (age, height, weight, etc.)
* Automatically calculated:

  * Daily calorie requirements
  * Protein requirements
  * BMI
* Store personal health data
* Track daily calorie and protein intake

---

## 🧩 System Modules

* Calorie Calculator
* Protein Requirement Calculator
* BMI Calculator
* User Authentication System
* Nutrition Tracking System

---

## 🗄️ Database Design

### Authentication System

Uses Django’s built-in authentication system for secure user login and registration.

### UserInfo Table

* Stores additional user details (age, height, weight)
* Connected to the User model using a **One-to-One relationship**
* Uses **ON DELETE CASCADE** to maintain data consistency

### Food Database

Contains approximately 20 food items with:

* Dish Name
* Serving Size
* Calories
* Protein Content

This helps users efficiently track their daily nutritional intake.

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite (Django ORM)
* **Authentication:** Django Built-in Authentication System

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/kamran696-pixel/fitzy_project.git
cd fitzy_project
python -m venv venv
venv\Scripts\activate   # For Windows
pip install -r requirements
python manage.py migrate
python manage.py runserver
```

Then open:
http://127.0.0.1:8000/

---


## 👨‍💻 Author

**Kamran**
GitHub: https://github.com/kamran696-pixel
