# 📚 LCU Book Bank — Django

A student-driven academic resource platform for Lead City University.
Built with Django and styled with a modern, high-contrast, eye-friendly design. Submissions go straight to the database — review and approve in the custom Unfold admin dashboard to go live instantly.

---

## ⚡ Local Setup (do this once)

### 1. Prerequisites
Make sure you have Python 3.11+ installed.
```bash
python --version   # should say 3.11 or higher
```

### 2. Clone / Navigate to the project
```bash
git clone https://github.com/Bkfactor/bookbank-django.git
cd bookbank-django
```

### 3. Create a virtual environment
```bash
python -m venv venv

# Activate it:
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Mac/Linux:
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up your `.env` file
```bash
cp .env.example .env
```
- Open `.env` and set `SECRET_KEY` to a random secret string.
- Leave `DATABASE_URL` blank for local development — it defaults automatically to SQLite (`db.sqlite3`).
- For direct document uploads to function, provide your Cloudinary credentials (`CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`).

### 6. Run migrations (creates the database tables)
```bash
python manage.py migrate
```

### 7. Seed all 10 faculties and 101 department entries
```bash
python manage.py seed_faculties
```
This command populates the database with all 10 faculties (Natural & Applied Sciences, Engineering & Technology, Law, Social Management & Sciences, Communication & Information Science, Environmental Design & Management, Arts & Education, Medicine & Health Sciences, Pharmacy, and General Studies) and their respective departments based on official university structures.

### 8. Create your admin account
```bash
python manage.py createsuperuser
```
Pick a username, email, and password. This will be your login for the admin dashboard.

### 9. Start the server
```bash
python manage.py runserver
```

- Web App: **http://127.0.0.1:8000**
- Admin Dashboard: **http://127.0.0.1:8000/admin**

---

## 🔄 Core Workflows

### 1. Material Submission & Moderation
```
Student fills form at /upload/
(Uploads file directly via Cloudinary OR pastes a Google Drive link)
        ↓
Resource saved to database with status = "pending"
        ↓
Admin opens /admin/ → Resources
        ↓
Review & click "Approve" (or batch select → "Approve selected")
        ↓
Status becomes "approved" → appears LIVE on the site immediately
```

### 2. Rating & Review System
- **1–5 Star Ratings**: Submitted anonymously via student sessions without requiring an account. Average ratings are calculated dynamically.
- **Written Reviews**: Allows students to leave feedback on course materials. Reviews are moderated by default to prevent spam before appearing under the resource card.

### 3. Student Feedback & Academic Concern Desk
- Available at `/feedback/`.
- Enables students to report missing study resources, report broken links, lodge academic concerns, or provide suggestions.
- All submissions appear directly in the admin dashboard under the **Feedback** module with actionable statuses (`Pending`, `In Progress`, `Resolved`).

---

## 🛠️ Student Tools Toolkit

The Book Bank includes a client-side suite of academic productivity tools for students that run locally in the browser (`localStorage`):

- **CGPA Calculator** (`/tools/cgpa-calculator/`): Semester GPA and cumulative CGPA calculation based on a 5.0 scale.
- **Target CGPA Calculator** (`/tools/target-cgpa/`): Calculates the target grades required in future semesters to reach a target degree class.
- **APA Citation Generator** (`/tools/citation-generator/`): Generates APA 7th edition bibliographic citations for books and web resources.
- **Flashcards** (`/tools/flashcards/`): Digital flashcard deck creator for quick revision.
- **Exam Tracker** (`/tools/exam-tracker/`): Visual countdown clock and schedule tracker for tests and exams.
- **Study Hub** (`/tools/study-hub/`): Pomodoro focus timer with ambient background audio integration.

---

## 🚀 Deployment (Vercel + Neon PostgreSQL)

The project is structured for serverless deployment on **Vercel** with a managed **Neon PostgreSQL** cloud database.

### 1. Configure Vercel Environment Variables
In your Vercel Project Dashboard (**Settings** → **Environment Variables**):

| Variable | Description |
| :--- | :--- |
| `SECRET_KEY` | Strong random secret key |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.vercel.app` (and your custom domain) |
| `DATABASE_URL` | Your Neon PostgreSQL connection string (`postgresql://...`) |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary Cloud Name for file uploads |
| `CLOUDINARY_API_KEY` | Cloudinary API Key |
| `CLOUDINARY_API_SECRET` | Cloudinary API Secret |

### 2. Running Production Migrations & Seeding
To apply database migrations or seed departments on the remote Neon database from your local machine:
```powershell
# Windows PowerShell
$env:DATABASE_URL="your-neon-database-url"
venv\Scripts\python.exe manage.py migrate
venv\Scripts\python.exe manage.py seed_faculties
```

---

## 📁 Project Structure

```
bookbank-django/
├── bookbank/               Django project configuration
│   ├── settings.py         Settings (handles SQLite locally & PostgreSQL in production)
│   ├── urls.py             Root routing
│   └── wsgi.py             WSGI application entry
├── core/                   Main application
│   ├── models.py           Faculty, Department, Resource, Rating, Review, Feedback
│   ├── views.py            Views for resources, faculties, search, upload, reviews, feedback, tools
│   ├── admin.py            Unfold admin configuration and moderation actions
│   ├── dashboard.py        Custom analytics and metrics callback for Unfold admin
│   ├── forms.py            Forms for resource upload and student feedback
│   ├── urls.py             App routing
│   └── management/
│       └── commands/
│           └── seed_faculties.py  Populates faculties and departments
├── templates/
│   ├── admin/index.html    Customized Unfold dashboard template
│   └── core/               Frontend templates (home, faculty, upload, tools, material cards)
├── static/
│   ├── css/style.css       Theme styling (dark & light mode compliant)
│   └── js/                 Interactive frontend utilities
├── requirements.txt        Python dependencies (Django, Unfold, Cloudinary, Whitenoise, etc.)
└── .env.example            Environment configuration template
```

---

## 🛠 Common Management Commands

| Task | Command |
| :--- | :--- |
| Start development server | `python manage.py runserver` |
| Make new migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Seed faculties and departments | `python manage.py seed_faculties` |
| Create admin user | `python manage.py createsuperuser` |
| Collect static files | `python manage.py collectstatic --noinput` |

---

Built by **Amb. Benjamin Erenose Omonkhodion** · LCU Student Ambassador Team  
Official Platform: [bookbanklcu.vercel.app](https://bookbanklcu.vercel.app)
