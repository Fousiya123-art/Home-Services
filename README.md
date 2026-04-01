🏠 Home Services Marketplace (Django Project)
📌 Project Overview

The Home Services Marketplace is a web-based application developed using Django. It allows users to browse, search, and book various home services such as cleaning, electrical work, AC repair, and more.

🎯 Features
👤 User Features
User Registration & Login
Browse service categories
View service details
Add services to cart
Book services
Chat with service providers
🛠️ Admin Features
Add/Edit/Delete services
Manage categories
View user bookings
Upload service images
🏗️ Tech Stack
Backend: Django (Python)
Frontend: HTML, CSS
Database: SQLite
Version Control: Git & GitHub
📂 Project Structure
HomeServices/
│
├── marketplace/
│   ├── templates/
│   │   ├── home.html
│   │   ├── services.html
│   │   ├── serviceview.html
│   │   ├── cart.html
│   │   ├── signup.html
│   │   └── chat.html
│   │
│   ├── static/
│   │   ├── css/
│   │   └── images/
│   │
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── uploads/
├── db.sqlite3
├── manage.py
└── README.md
⚙️ Installation & Setup

1️⃣ Clone the Repository
git clone https://github.com/Fousiya123-art/Home-Services.git
cd Home-Services
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install django
4️⃣ Run Migrations
python manage.py migrate
5️⃣ Run Server
python manage.py runserver
6️⃣ Open in Browser
http://127.0.0.1:8000/
🔐 Admin Access

Create admin user:

python manage.py createsuperuser

Login at:
http://127.0.0.1:8000/admin/
