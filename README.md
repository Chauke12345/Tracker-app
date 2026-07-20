# 📊 Tracker App

A Django-based Expense Tracker Web Application that helps users manage income and expenses, track balances, analyze financial activity, and import transactions from bank statements.

The application provides a simple and user-friendly interface for monitoring personal finances with automated financial analytics.

---

## ✨ Features

* ➕ Add income and expense transactions
* 🏷️ Categorize financial entries
* 💰 Track total income, expenses, and current balance
* 📊 Monthly income and expense analytics
* 📜 View complete transaction history
* 📄 Upload bank statements
* 📥 Import transactions from CSV, Excel, and PDF files
* 🔐 User authentication and personal accounts
* 🛠️ Django admin panel for database management
* ☁️ Production deployment on Render

---

## 🛠 Tech Stack

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* Bootstrap

### Database

* PostgreSQL (Production)
* SQLite (Local Development)

### Data Processing

* Pandas
* OpenPyXL
* PDFPlumber

### Deployment

* Render
* Gunicorn
* WhiteNoise

---

## 📁 Project Structure

```bash
Tracker-app/

│
├── manage.py
│
├── expense_tracker/        # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tracker/                # Main expense tracking application
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── templates/              # HTML templates
│
├── static/                 # CSS, JavaScript and static files
│
├── requirements.txt        # Python dependencies
│
└── manage.py
```

---

## 🚀 Deployment

The application is deployed using Render with:

* PostgreSQL database
* Gunicorn application server
* WhiteNoise static file handling
* Environment variables for production settings

---

## 📌 Future Improvements

* Automatic bank transaction categorization
* Budget planning
* Financial reports export
* More advanced analytics dashboards
* Mobile-friendly improvements

---

## 👨‍💻 Developer

**Miehleketo E. Chauke**

Junior Full-Stack Developer
Python | Django | JavaScript | PostgreSQL

```
```
