# 📚 Book-Review  
[**Live Demo**](https://product-scrapper-gjlp.onrender.com/)

A Django-based web application that allows users to register and log in using JWT authentication and perform full CRUD operations on books and their reviews. Only authenticated users can add books, write reviews, and manage their own content.

---

## ✨ Features

- **User Authentication**
  - Register, login, and logout with JWT-based security.
- **Books Management**
  - Add, view, update, and delete books.
- **Reviews System**
  - Write and manage reviews for books (only for logged-in users).
- **Book Detail Pages**
  - View detailed information about each book at `/product/<id>/`.
- **Admin Panel**
  - Built-in Django admin support for managing users, books, and reviews.

---

## 🛠 Tech Stack

- **Backend**: Django, Django REST Framework (DRF)
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: Django templates (HTML, CSS)
- **Styling**: Tailwind CSS (stored in `static/`)
- **Database**: SQLite (default `db.sqlite3`)
- **Server**: Gunicorn (for deployment)

---

## 🚀 Getting Started (Windows / PowerShell)

Follow these steps to run the project locally:

1) Clone and navigate:
git clone <this-repo-url>
cd bookstore


2) Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\Activate.ps1


3) Install dependencies:
pip install -r requirements.txt


4) Apply migrations:
python manage.py migrate


6) Create a superuser (optional, for admin):
python manage.py createsuperuser


7) Run the dev server:
python manage.py runserver


Visit:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
 
