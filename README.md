# 📝 Personal Blog Project (Flask)

A **personal blogging web application** built with **Flask**.  
This project demonstrates user authentication, post management, database integration, RESTful API development, and email functionality — all in one cohesive web app.

---

## 🚀 Features

- 🧾 **Post Management** – Create, edit, and delete blog posts  
- 👥 **User Authentication** – Register and log in securely with password hashing  
- 💬 **User & Post Interaction** – Manage authors and their posts easily  
- ⚙️ **Database Integration** – Built with **SQLAlchemy ORM**  
- 🔐 **Password Hashing** – Secure password storage with hashing  
- 🌐 **RESTful API** – Manage blog posts through a REST API  
- 📧 **Email Support** – Send emails using Flask-Mail and SMTP  
- 🧠 **Version Control** – Fully managed using **Git & GitHub**

---

## 🧱 Project Structure
FlaskBlog/
├── static/ # CSS, JS, and image files
├── templates/ # HTML templates
├── app.py # Main Flask application
├── models.py # SQLAlchemy models
├── forms.py # WTForms for registration & login
├── routes.py # Route definitions
├── config.py # Configuration settings (DB, email, etc.)
├── api.py # REST API endpoints
└── README.md

yaml
Copy code

---

## ⚙️ Technologies Used
- **Flask** – Web framework  
- **Flask-SQLAlchemy** – ORM for database management  
- **Flask-WTF** – Form handling and validation  
- **Flask-Login** – User session management  
- **Flask-Mail** – Email integration  
- **SQLite / PostgreSQL** – Database  
- **HTML / CSS / Bootstrap** – Frontend  
- **GitHub** – Version control  

---

## 🧰 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/FlaskBlog.git
cd FlaskBlog
2. Create a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file and set up your configuration:

ini
Copy code
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///site.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
5. Initialize the Database
bash
Copy code
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
6. Run the Application
bash
Copy code
flask run
Visit the app at:
👉 http://127.0.0.1:5000/

🌐 API Endpoints
Method	Endpoint	Description
GET	/api/posts	Get all posts
GET	/api/posts/<id>	Get a single post
POST	/api/posts	Create a new post
PUT	/api/posts/<id>	Update a post
DELETE	/api/posts/<id>	Delete a post

📬 Email Functionality
The app supports email sending via Flask-Mail.
It can be used for:

User registration confirmation

Password reset

Contact form messages

🧑‍💻 Version Control
All versions and updates of this project are tracked via GitHub.
To check commit history:

bash
Copy code
git log --oneline
📜 License
This project is licensed under the MIT License — feel free to use and modify it.

