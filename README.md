# 📚 LCU Book Bank — Django

A student-driven academic resource platform for Lead City University.
Built with Django. Submissions go straight to the database — approve in admin, go live instantly.

---

## ⚡ Local Setup (do this once)

### 1. Prerequisites
Make sure you have Python 3.11+ installed.
```bash
python --version   # should say 3.11 or higher
```

### 2. Clone / extract the project
```bash
cd Desktop
# If you downloaded the zip, extract it, then:
cd bookbank-django
```

### 3. Create a virtual environment
```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up your .env file
```bash
cp .env.example .env
```
Open `.env` and replace `SECRET_KEY` with any long random string.
Leave `DATABASE_URL` blank — it will use SQLite locally (zero setup).

### 6. Run migrations (creates the database)
```bash
python manage.py migrate
```

### 7. Seed all 10 faculties and 85 departments
```bash
python manage.py seed_faculties
```
This populates the database with every faculty, department, and Drive link in one command.

### 8. Create your admin account
```bash
python manage.py createsuperuser
```
Pick a username, email, and password. This is your admin login.

### 9. Start the server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** — the site is live locally.
Open **http://127.0.0.1:8000/admin** — your admin dashboard.

---

## 🔄 The Submission Workflow (why Django solves your problem)

```
Student fills form at /upload/
        ↓
Resource saved to DB with status = "pending"
        ↓
You open /admin/ → Resources → see it listed
        ↓
You click Approve (or select multiple → "Approve selected")
        ↓
Status becomes "approved" → appears LIVE on the site instantly
```

No Google Form. No Google Sheet. No editing data.js. No redeployment.

---

## 🛠️ Student Tools Toolkit

The Book Bank includes a suite of built-in, privacy-first academic tools for students. These tools run entirely client-side using JavaScript and `localStorage`, ensuring no user data is saved to the backend.

- **CGPA Calculator** (`/tools/cgpa-calculator/`): Instantly calculate semester GPA based on a 5.0 scale.
- **Target CGPA Calculator** (`/tools/target-cgpa/`): Determines the required semester GPA to reach a target CGPA.
- **APA Citation Generator** (`/tools/citation-generator/`): Generates APA 7th edition citations for books and websites.
- **Flashcards** (`/tools/flashcards/`): Create and study custom digital flashcards.
- **Exam Tracker** (`/tools/exam-tracker/`): Track upcoming deadlines with visual countdowns and browser notifications.
- **Study Hub** (`/tools/study-hub/`): Pomodoro timer integrated with ambient YouTube streams (e.g., Lofi Girl).

---

## 🚀 Deploying to Vercel

The project is configured for deployment on Vercel.

### 1. Push to GitHub
```bash
git add .
git commit -m "Update"
git push origin main
```

### 2. Deploy on Vercel
1. Go to **vercel.com** → Add New Project
2. Import your GitHub repository (`bookbank-django`).
3. Vercel will auto-detect the Django project (assuming you have a `vercel.json` configured).
4. Add your Environment Variables in the Vercel dashboard:
   - `SECRET_KEY`
   - `DEBUG = False`
   - `ALLOWED_HOSTS = .vercel.app` (or your custom domain)

*Note: Vercel offers serverless functions, meaning SQLite is read-only in production. For a fully functional database on Vercel, connect a PostgreSQL database (like Supabase or Neon) and set your `DATABASE_URL`.*

---

## 📁 Project Structure

```
bookbank-django/
├── bookbank/           Django project config
│   ├── settings.py
│   └── urls.py
├── core/               Main app
│   ├── models.py       Faculty, Department, Resource, Review
│   ├── views.py        All page logic
│   ├── admin.py        Admin panel (approve/reject here)
│   ├── forms.py        Submission + review forms
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed_faculties.py   ← run once to populate DB
├── templates/core/     All HTML pages
├── static/css/         v8 styles (navy + gold)
├── requirements.txt
├── Procfile            Railway/Render deployment
└── .env.example        Copy to .env for local config
```

---

## 🛠 Common Commands

| Task | Command |
|------|---------|
| Start dev server | `python manage.py runserver` |
| Apply model changes | `python manage.py makemigrations && python manage.py migrate` |
| Seed faculties/depts | `python manage.py seed_faculties` |
| Create admin user | `python manage.py createsuperuser` |
| Collect static files | `python manage.py collectstatic` |

---

## ➕ Adding a Material Manually (from admin)

1. Go to `/admin/` → Resources → Add Resource
2. Fill in title, type, faculty, department, level, Drive URL
3. Set status to **Approved — Live**
4. Save → appears on site immediately

---

Built by Amb. Benjamin Erenose Omonkhodion · LCU Student Ambassador Team
