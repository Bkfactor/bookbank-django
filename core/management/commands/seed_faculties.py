"""
Seed the database with all LCU faculties and departments.
Sources: Official LCU website (lcu.edu.ng) — scraped October 2026
    python manage.py seed_faculties
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Faculty, Department

FACULTY_DATA = [

    # =========================================================================
    # 1. FACULTY OF NATURAL & APPLIED SCIENCES (FONAS)
    # Source: lcu.edu.ng/index.php/template/pages/overview
    # =========================================================================
    {
        "name": "Faculty of Natural & Applied Sciences",
        "abbr": "FONAS", "emoji": "🧪",
        "degree": "B.Sc", "color": "#16a34a", "order": 1,
        "drive_url": "https://drive.google.com/drive/folders/1AMFcGGdT8dswBLptKsJDyHBedjFb8IuH",
        "description": "Science, computing and IT students — notes, past questions and slides, all right here.",
        "departments": [
            ("All Departments (General)",              ""),
            ("Biochemistry",                           "https://drive.google.com/drive/folders/1OsWpKY12FUobPlD4__CZHZKx_o4gvPLb"),
            ("Biology",                                "https://drive.google.com/drive/folders/1z0qljymGae8Sa2796_U3LQems-FoA1za"),
            ("Biotechnology",                          ""),
            ("Chemistry",                              "https://drive.google.com/drive/folders/1uViW7Z43ArYgFXuQxdccm6SrbPClukk6"),
            ("Computer & Information Science",         "https://drive.google.com/drive/folders/17hrzCz8n6e2ZksXkccTjQ2sCA2B9DDRf"),
            ("Computer Science with Economics",        "https://drive.google.com/drive/folders/1-tUGl0LI-lda0jHtszDthahKJO3jVjUu"),
            ("Computer Science with Electronics",      "https://drive.google.com/drive/folders/1UyTnT9ieBwDUzMiub5PLx6YzbBYoS0Fx"),
            ("Cyber Security",                         "https://drive.google.com/drive/folders/18UKInWRHVNB8vR47LtpEQA7oQdQfswwJ"),
            ("Environmental Management & Toxicology",  "https://drive.google.com/drive/folders/1dc42_DL9nt_Jp4Z3ESviU-D2Gw_J9EZJ"),
            ("Forensic Science",                       "https://drive.google.com/drive/folders/10_4vgzL7fq5GNUEHNuMRRaHfe8EntrS4"),
            ("Geology",                                ""),
            ("Information Systems",                    "https://drive.google.com/drive/folders/1z3aGsK0iLJZOuqUj8uBVOjLp2jf_DrHa"),
            ("Information Technology",                 "https://drive.google.com/drive/folders/1wp0bdl-V3GjGhNhiuR2FwWkXmXpMJRIE"),
            ("Microbiology & Parasitology",            "https://drive.google.com/drive/folders/1zFPlsKJo57SU7-0aykJYCGxYd4dJeU5M"),
            ("Physics",                                "https://drive.google.com/drive/folders/1c68igR5hODqKuQC1QZfE1Yx4nEmJV4at"),
            ("Physics with Electronics",               "https://drive.google.com/drive/folders/1FXM5FtndbHAiW-T0rDo_Gmi8SaD1IkeD"),
            ("Science Laboratory Technology",          "https://drive.google.com/drive/folders/1twYtraHdOpl4d-rv0hgbWsmhMQn0sUk4"),
            ("Software Engineering",                   "https://drive.google.com/drive/folders/18_gHum3hc9NZlr0NcEOzLhrHQTsZVcPF"),
        ]
    },

    # =========================================================================
    # 2. FACULTY OF ENGINEERING & TECHNOLOGY (FENG)
    # Source: lcu.edu.ng/index.php/template/template-features-2/overview
    # =========================================================================
    {
        "name": "Faculty of Engineering & Technology",
        "abbr": "FENG", "emoji": "⚙️",
        "degree": "B.Eng", "color": "#d97706", "order": 2,
        "drive_url": "https://drive.google.com/drive/folders/1peMRXqufqmXVvxfu0FcuspV002ttO4-R",
        "description": "Engineering students — past papers, lab reports and lecture slides, organised by department.",
        "departments": [
            ("All Departments (General)",           ""),
            ("Biomedical Engineering",              ""),
            ("Civil Engineering",                   "https://drive.google.com/drive/folders/1tVPRURvx6N7IHmH1dg_KaGaVLRPeErMA"),
            ("Electrical & Electronic Engineering", "https://drive.google.com/drive/folders/1D9TlhwDzhJNLQMJyroUwFEEvkYX5j7Qx"),
            ("Mechanical Engineering",              "https://drive.google.com/drive/folders/1eCGLGYbN3WiO_idVML-yioUzt9tOtI6p"),
            ("Mechatronics Engineering",            ""),
            ("Wood Products Engineering",           "https://drive.google.com/drive/folders/1-h4G4tgzBz8wKi1tNN1OS-dbDNijANG9"),
        ]
    },

    # =========================================================================
    # 3. FACULTY OF LAW (FLAW)
    # Note: Kept as-is despite suspension — students still in class
    # =========================================================================
    {
        "name": "Faculty of Law",
        "abbr": "FLAW", "emoji": "⚖️",
        "degree": "LLB / BLD", "color": "#7c3aed", "order": 3,
        "drive_url": "https://drive.google.com/drive/folders/1OGBD9sh-XuFhVveetCf5nEG11SEFczhb",
        "description": "Law students — case summaries, moots, past bar prep and more, all in one place.",
        "departments": [
            ("All Departments (General)", ""),
            ("Bachelor of Laws (LLB)",    "https://drive.google.com/drive/folders/1zfdix8GPE6z6fwGFu0a430ubnOuTSAuk"),
            ("Law & Diplomacy (BLD)",     "https://drive.google.com/drive/folders/1GZQ6C4L9xuPN6MTIg-p0ZwrRB3jBwKaY"),
        ]
    },

    # =========================================================================
    # 4. FACULTY OF SOCIAL MANAGEMENT & SCIENCES (MSS)
    # Source: lcu.edu.ng/index.php/template/typography/overview
    # =========================================================================
    {
        "name": "Faculty of Social Management & Sciences",
        "abbr": "MSS", "emoji": "📊",
        "degree": "B.Sc", "color": "#0891b2", "order": 4,
        "drive_url": "https://drive.google.com/drive/folders/1QgdipQrXF8v_1jDpqBqcmsE8qE0m53gE",
        "description": "Accounting, Business, Economics or Social Sciences? Your notes, past questions and textbooks are here.",
        "departments": [
            ("All Departments (General)",                            ""),
            ("Accounting",                                           "https://drive.google.com/drive/folders/12CRp3_XeyWVEHlJ1i5HPE57qu6GCw6GX"),
            ("Banking & Finance",                                    "https://drive.google.com/drive/folders/1fNgLqDkvkPOzzY5hW1cz55fP9RGQoQQW"),
            ("Business Administration",                              "https://drive.google.com/drive/folders/1ZrLCkI2wRDvCEz1ue4WVG_1ydHP8KHC9"),
            ("Criminology & Security Studies",                       "https://drive.google.com/drive/folders/19Rr-aIQAUF-dP_gALGd1euodauH-pyeX"),
            ("Economics & Development Studies",                      "https://drive.google.com/drive/folders/1HEIO0haAu5UWqjKQYHpYK-w-cMQSx2iw"),
            ("Entrepreneurship",                                     "https://drive.google.com/drive/folders/1A6wTu3_G42WSXQVjKuVbDKS5ly-BD7YZ"),
            ("International Relations & Human Resource Management",  "https://drive.google.com/drive/folders/10JREozQoaHu-GPjDvZBgRGtoFFx9si63"),
            ("Marketing",                                            "https://drive.google.com/drive/folders/1bV0APyZTOz45ejV0p8nM9bk43w7mnasV"),
            ("Politics & International Relations",                   "https://drive.google.com/drive/folders/1sdHspp42ec8VcW27ofkOOA-yCBS_o0Gd"),
            ("Psychology",                                           "https://drive.google.com/drive/folders/1qcKn3lKoY3_rTgUQey5FKM6mseayA8yb"),
            ("Public Administration",                                "https://drive.google.com/drive/folders/1GahStSjWy7pqfl3f6eyQMT-njqloNvjZ"),
            ("Social Work",                                          "https://drive.google.com/drive/folders/1sSaCECfsdBZi1Iypt8Z6SQncveSOSolD"),
            ("Sociology",                                            "https://drive.google.com/drive/folders/145HaFpHhJ2v2tUotnsNPpE7NR0GysohP"),
            ("Tourism & Hospitality Management",                     "https://drive.google.com/drive/folders/1hwrVggAz0aSYgydDzwueRd4ophsxzPcQ"),
        ]
    },

    # =========================================================================
    # 5. FACULTY OF COMMUNICATION & INFORMATION SCIENCE (ICS)
    # Source: lcu.edu.ng/index.php/template/cis/overview
    # =========================================================================
    {
        "name": "Faculty of Communication & Information Science",
        "abbr": "ICS", "emoji": "📡",
        "degree": "B.Sc", "color": "#db2777", "order": 5,
        "drive_url": "https://drive.google.com/drive/folders/1G_iwGwMMlxELrsDx90aHt400_gEbiqm-",
        "description": "Mass Comm, Media, Library or Office Management students — past questions and study materials right here.",
        "departments": [
            ("All Departments (General)",             ""),
            ("Advertising",                           "https://drive.google.com/drive/folders/1TUdPy-QO_i7RI578Rr-1nCuY7W5xBr6f"),
            ("Information Resources Management",      ""),
            ("Journalism",                            "https://drive.google.com/drive/folders/12FdWl0O7krEIDOSX3j8MlnYHLH3LoSnq"),
            ("Library and Information Science",       "https://drive.google.com/drive/folders/1vG3OzaW6MoqDDOjiFdOmN4gZ2Lu-72HZ"),
            ("Mass Communication & Media Technology", "https://drive.google.com/drive/folders/1DEZEtkvXl2KrTKpZB1sT4Se3BUY00-bx"),
            ("Media Studies",                         "https://drive.google.com/drive/folders/1v2YCUeZLv6C8tLWDtPvc8kv45QoHVmrA"),
            ("Office and Information Management",     "https://drive.google.com/drive/folders/18GsPEMMq3fQazdUmE2K2ruoE_FD1iPwy"),
            ("Printing and Publishing",               "https://drive.google.com/drive/folders/1FCGVg-2zLLDB8utVnuhygLMNUKOCdNFG"),
            ("Public Relations",                      "https://drive.google.com/drive/folders/1ZlldvAW2eLjszoq4JVYiAH2-qdxGnZvr"),
        ]
    },

    # =========================================================================
    # 6. FACULTY OF ENVIRONMENTAL DESIGN & MANAGEMENT (FEDM)
    # Source: lcu.edu.ng/index.php/template/typography-2/overview-fedm
    # =========================================================================
    {
        "name": "Faculty of Environmental Design & Management",
        "abbr": "FEDM", "emoji": "🏗️",
        "degree": "B.Sc / B.Arch", "color": "#ea580c", "order": 6,
        "drive_url": "https://drive.google.com/drive/folders/1-jczQm9rH9dxMPnsww5p-Y7PoBDoEDsc",
        "description": "Architecture, Planning and Built Environment students — design briefs, notes and past questions all in one place.",
        "departments": [
            ("All Departments (General)",       ""),
            ("Architecture",                    "https://drive.google.com/drive/folders/16pp00W_LXsu9LEJvSmu09aLjh1pBdSFO"),
            ("Building",                        "https://drive.google.com/drive/folders/1TFzfdXhrc85dio2XnTlI_fL-rXIMXn6g"),
            ("Estate Management",               "https://drive.google.com/drive/folders/1OBavcUcGeZ_js9VHEfbnnCx4Eu-8YIAv"),
            ("Fine and Applied Arts & Design",  ""),
            ("Geographic Information Science",  ""),
            ("Surveying and Geoinformatics",    "https://drive.google.com/drive/folders/146OtBUVafkK1G-gCUWluH1uXPXZxIiJl"),
            ("Urban and Regional Planning",     "https://drive.google.com/drive/folders/1xrsdrDz3JKFITzhOsGdJKgGn3valt-8p"),
        ]
    },

    # =========================================================================
    # 7. FACULTY OF ARTS & EDUCATION (FARTS)
    # Source: lcu.edu.ng/index.php/template/2016-10-27-08-53-54/overview
    # =========================================================================
    {
        "name": "Faculty of Arts & Education",
        "abbr": "FARTS", "emoji": "📚",
        "degree": "B.A / B.Ed / B.Sc (Ed)", "color": "#9333ea", "order": 7,
        "drive_url": "https://drive.google.com/drive/folders/1RP2EpTZ_5ChHuCF5yrnGl2PHol8Uzwr-",
        "description": "Languages, Literature, Performing Arts and Education students — find all your study materials here.",
        "departments": [
            ("All Departments (General)",               ""),
            # --- B.A. (Arts) ---
            ("English",                                 "https://drive.google.com/drive/folders/1ScghG5cNsiSBIPR8O6Feyi_vWzXeNRFc"),
            ("English & Literary Studies",              "https://drive.google.com/drive/folders/1ScghG5cNsiSBIPR8O6Feyi_vWzXeNRFc"),
            ("English & French",                        ""),
            ("French",                                  ""),
            ("Fine Arts",                               ""),
            ("History & Diplomacy",                     ""),
            ("Performing Arts, Music & Film Studies",   "https://drive.google.com/drive/folders/1kfkbMRBsnEFKJqqHV9iRbdFGbTa-lvH9"),
            ("Religious Studies",                       "https://drive.google.com/drive/folders/1cJCFsSpW0Yt1f1BhVlTHeneBJdZS8nlc"),
            ("Yoruba (African Languages)",              ""),
            # --- B.Sc (Ed) ---
            ("Biology Education",                       "https://drive.google.com/drive/folders/1W-zUBkboKYhXYzjvxcNU1Ga3PdLAN6bZ"),
            ("Chemistry Education",                     "https://drive.google.com/drive/folders/1zDh-_DkoAzrcSYfV7JWP6-O4Qnx5ck5_"),
            ("Computer Science Education",              "https://drive.google.com/drive/folders/1oy04CxDgujisWh9zma-hQNP-BV87fBwC"),
            ("Mathematics Education",                   "https://drive.google.com/drive/folders/1aa2XRl1LFZOC5H6wOJjnxtB3JKob37iD"),
            ("Physics Education",                       "https://drive.google.com/drive/folders/14cpYWFliNIsyEA0LSEdpFG8NCFOZJLgd"),
            # --- B.A. (Ed) ---
            ("English Language Education",              "https://drive.google.com/drive/folders/1LLZu_X6cV7DfWV-0Lyok47y9tSHKcr1m"),
            ("Education",                               ""),
            # --- B.Ed ---
            ("Business Education",                      "https://drive.google.com/drive/folders/1G35s4ujK2W94xlVMGPD8J8L7nbSnqVUw"),
            ("Early Childhood Education",               ""),
            ("Economics Education",                     ""),
            ("Educational Management",                  "https://drive.google.com/drive/folders/1q9SoNNZj8hk_hlYteCVpP_WF-EnMqR3T"),
            ("Guidance & Counselling",                  ""),
            ("Kinesiology & Physical and Health Education", "https://drive.google.com/drive/folders/1nfdGORBvsa2VbdTGP5L6g_SEsznTHzoA"),
            ("Social Studies Education",                "https://drive.google.com/drive/folders/1su5I5avcc-BYz4HYTjzPT2oFVDolvEMV"),
        ]
    },

    # =========================================================================
    # 8. COLLEGE OF MEDICINE & HEALTH SCIENCES (COM)
    # Source: lcu.edu.ng/index.php/template/cm-hs/overview
    # =========================================================================
    {
        "name": "College of Medicine & Health Sciences",
        "abbr": "COM", "emoji": "🩺",
        "degree": "MBBS / B.Sc / DPT", "color": "#dc2626", "order": 8,
        "drive_url": "https://drive.google.com/drive/folders/1rTuz1ZLGiE-mudSJdAnLhfrpN0ScnJrA",
        "description": "Medical and health science students — anatomy notes, past questions and clinical resources, organised for you.",
        "departments": [
            ("All Departments (General)",       ""),
            ("Community Health Sciences",       "https://drive.google.com/drive/folders/1su_3sczAi8baIUm87T8sXL_RYdwpR4Gi"),
            ("Dental Technology",               ""),
            ("Dental Therapy",                  ""),
            ("Dentistry",                       "https://drive.google.com/drive/folders/1KVZ7d9sIf6xe6IQY9Odzg6rjgy-gnVA1"),
            ("Health Information Management",   "https://drive.google.com/drive/folders/1FZyvZscClkxfjmyYNOqUM8ikNAO1q-1A"),
            ("Human Anatomy",                   "https://drive.google.com/drive/folders/1LAtoiIn_8ZyrvkGcmTRufLnb9Y5R_SdQ"),
            ("Human Nutrition & Dietetics",     "https://drive.google.com/drive/folders/12drmc8Op7uhubL-cfSQ9jR9sK8Iw77Sk"),
            ("Medical Laboratory Sciences",     "https://drive.google.com/drive/folders/1AeHkYEHm_I-rhGEsY_yU1cKrOGqFlHGC"),
            ("Medicine and Surgery (MBBS)",     "https://drive.google.com/drive/folders/1mOPTCIs_u5cZEqW3sqWHuwdG9bTTs5lU"),
            ("Nursing",                         "https://drive.google.com/drive/folders/1uglw8uhyRiyt2o46aDHDrk-04cejhAY9"),
            ("Physiotherapy",                   "https://drive.google.com/drive/folders/1WnWjdx8a42ImNS4inn-EEey5rljuaJvL"),
            ("Physiology",                      "https://drive.google.com/drive/folders/1k17D0mKSRu70IgFWvXTIdccjL0GoVXpb"),
            ("Public Health",                   ""),
            ("Radiography",                     "https://drive.google.com/drive/folders/1EhoxmvnQUXB994ct_OL7I0n32TcuHtQ_"),
        ]
    },

    # =========================================================================
    # 9. FACULTY OF PHARMACY (FPHARM)
    # Source: lcu.edu.ng/index.php/template/faculty-of-pharmacy/overview
    # =========================================================================
    {
        "name": "Faculty of Pharmacy",
        "abbr": "FPHARM", "emoji": "💊",
        "degree": "Pharm.D", "color": "#0891b2", "order": 9,
        "drive_url": "https://drive.google.com/drive/folders/1R8PFt-3VvLe2HJmPo2_44A2r-grpiw6M",
        "description": "Pharmacy students — drug notes, past questions and clinical study materials right here.",
        "departments": [
            ("All Departments (General)",                   ""),
            ("Doctor of Pharmacy (Pharm.D)",                "https://drive.google.com/drive/folders/10kxbnCjnMFwDbV5I_yClD77jcUP47skF"),
        ]
    },

    # =========================================================================
    # 10. GENERAL STUDIES (GST)
    # =========================================================================
    {
        "name": "General Studies (GST)",
        "abbr": "GST", "emoji": "🌐",
        "degree": "General", "color": "#475569", "order": 10,
        "drive_url": "",
        "description": "University-wide courses taken across all departments and faculties (e.g. GST 111, GST 112).",
        "departments": [
            ("All Departments (General)", ""),
        ]
    },
]


class Command(BaseCommand):
    help = "Seed all LCU faculties and departments into the database"

    def handle(self, *args, **kwargs):
        created_f = created_d = updated_d = 0

        for f_data in FACULTY_DATA:
            faculty, f_new = Faculty.objects.update_or_create(
                abbr=f_data["abbr"],
                defaults={
                    "name":        f_data["name"],
                    "slug":        slugify(f_data["name"]),
                    "emoji":       f_data["emoji"],
                    "degree":      f_data["degree"],
                    "color":       f_data["color"],
                    "order":       f_data["order"],
                    "drive_url":   f_data["drive_url"],
                    "description": f_data["description"],
                }
            )
            if f_new:
                created_f += 1
                self.stdout.write(f"  + Faculty: {faculty.name}")
            else:
                self.stdout.write(f"  ~ Updated: {faculty.name}")

            # Build set of valid slugs for this faculty from seed data
            valid_slugs = {slugify(name) for name, _ in f_data["departments"]}

            for i, (dept_name, dept_url) in enumerate(f_data["departments"]):
                dept, d_new = Department.objects.update_or_create(
                    faculty=faculty,
                    slug=slugify(dept_name),
                    defaults={
                        "name":      dept_name,
                        "drive_url": dept_url,
                        "order":     i,
                    }
                )
                if d_new:
                    created_d += 1
                    self.stdout.write(f"      + Dept: {dept_name}")
                else:
                    updated_d += 1

            # NOTE: We intentionally do NOT delete old departments here.
            # Departments have CASCADE-linked Resources — deleting a department
            # would permanently destroy all uploaded documents under it.
            # To retire a department, do it manually via the admin panel
            # after reassigning or archiving its resources.

        self.stdout.write(
            f"\nDone -- {created_f} new faculties, {created_d} new departments, "
            f"{updated_d} updated"
        )
