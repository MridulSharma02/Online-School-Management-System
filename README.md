# 🏫 Online School Management System

> A role-based school management web app built with Python & Streamlit.

---

## ✨ Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📌 Project Overview

A full-featured school management system with **three role-based portals**:

| Portal | Features |
|--------|----------|
| 🛡️ **Admin** | Manage students, teachers, fees & salary records |
| 👩‍🏫 **Teacher** | Upload marks, manage assignments, view salary |
| 🎓 **Student** | View report cards, progress graphs, pay fees |

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/school-management-system.git
cd school-management-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

---

## 🔐 Demo Credentials

| Role | User ID | Password |
|------|---------|----------|
| 🛡️ Admin | `alex@school.org` | `admin123` |
| 👩‍🏫 Teacher | `jordan@school.org` | `teach456` |
| 🎓 Student | `sam@school.org` | `student789` |

---

## 🛠️ Tech Stack

- **Frontend** — Streamlit + Custom CSS
- **Data** — Pandas (demo data; original uses MySQL)
- **Charts** — Matplotlib
- **Original backend** — Python 3.6 · MySQL · `mysql-connector-python`

---

## 📁 Project Structure

```
school-management-system/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 📊 Features

- **Report Cards** — Weekly tests, Half-yearly & Final exams with grade calculation
- **Progress Analysis** — Side-by-side bar charts comparing performance across all exams
- **Fee Management** — Quarterly fee payment tracking with late payment alerts
- **Salary Module** — Basic pay, allowances, tax (8%) & leave deductions
- **Assignment Tracker** — Subject-wise assignment submission status
- **CRUD Operations** — Add / Update / Delete for all entities

---

## ⚠️ Limitations (from original project)

- Password input is not masked in the original Python CLI version  
- This Streamlit version uses in-memory demo data (no live MySQL connection)

---

## 📚 Bibliography

1. https://stackoverflow.com/
2. https://www.geeksforgeeks.org
3. https://docs.python.org
4. https://docs.streamlit.io
