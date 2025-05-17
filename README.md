# 🧠 AI Attendance Backend

This is the backend system for an **AI-powered attendance application** that uses facial recognition to detect and mark attendance automatically. Built using **Django** and the **Django REST Framework (DRF)**, this backend provides APIs for user registration, authentication, attendance tracking, and real-time face recognition powered by an external model.

> ⚠️ To function properly, you **must download the required AI model** and place it in the appropriate directory. See [Model Setup](#model-setup) below.

---

## 🚀 Features

- 🔐 **User Authentication & Authorization**
- 📸 **Face Detection & Recognition** with an external executable model
- 🗓️ **Automated Attendance Marking**
- 👥 **Admin User Management**
- 📁 **Database Integration** using Django ORM

---

## 🧱 Tech Stack

- **Django** – High-level Python web framework  
- **Django REST Framework (DRF)** – Toolkit for building RESTful APIs  
- **OpenCV / face-recognition** – Face detection (via external AI model)  
- **SQLite / PostgreSQL** – Supported DB backends  
- **JWT / Token Auth** – User login & authentication  

---

## 🗂️ Project Structure (Simplified)

```

ai\_attendance\_backend/
├── attendance/           # Core app for attendance logic
├── authentication/       # Login, registration, user management
├── backend/              # Project settings and URLs
│   ├── settings.py
│   └── urls.py
├── dist/                 # 🔻 Place ai_model.exe here
├── manage.py
├── requirements.txt
└── .env

```

---

## 📥 Model Setup

The facial recognition system relies on an external model file.

### 🔗 Download the model:

[📦 ai_model.exe (Google Drive)](https://drive.google.com/file/d/1BxzTyj7K6EDJ0kLVx9l0f6Y_lRz8y8yb/view?usp=sharing)

### 📁 Place it in:

```

backend/api/dist/ai_model.exe

````

Without this file, the system **will not perform face recognition or mark attendance**.

---

## ▶️ Running the Server

### 1. Clone the repo and install dependencies:

```bash
git clone https://github.com/farrukhunites/ai_attendance_backend.git
cd ai_attendance_backend
pip install -r requirements.txt
````

### 2. Configure Environment

Create a `.env` file and add your Django settings (e.g., secret key, DB config).

### 3. Apply Migrations & Run

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

The app will be available at:
🌐 `http://localhost:8000`

---

## 🧠 How It Works (Flow)

1. **Admin registers a user** and stores face info
2. **User appears on camera**
3. Frame is sent to backend and passed to `ai_model.exe`
4. Face is matched and attendance is logged
5. Admin can view attendance history via API or frontend

---

## 🧰 Developer Notes

* 🔐 Use token-based auth or consider JWT for scalable API security
* 🧪 Add test coverage using `pytest` or Django’s test framework
* 📦 Consider Dockerizing the project for consistent deployment
* 🌍 Serve `ai_model.exe` through background process if needed

---

## 🙌 Contributing

Want to improve the system?
Open an issue or submit a PR!

---

## 🙋‍♂️ About Me

**Muhammad Farrukh Umair**  
Software Engineer | AI & Data Enthusiast

📫 **Email**: [haris.umair2002@gmail.com](mailto:haris.umair2002@gmail.com)  
🔗 **LinkedIn**: [linkedin.com/in/muhammad-farrukh-umair](https://www.linkedin.com/in/muhammad-farrukh-umair/)

---

## 🧾 License

This project is open-source and available under the [MIT License](LICENSE).
