"""
Run once to populate the database with all 10 faculties and 85 departments.
    python manage.py seed_faculties
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Faculty, Department

FACULTY_DATA = [
  {
    "name": "Natural & Applied Sciences", "abbr": "FONAS", "emoji": "🧪",
    "degree": "B.Sc", "color": "#16a34a", "order": 1,
    "drive_url": "https://drive.google.com/drive/folders/1AMFcGGdT8dswBLptKsJDyHBedjFb8IuH",
    "description": "Computing, Science or IT? Your notes, past questions and slides are all right here.",
    "departments": [
      ("Computer Science",                      "https://drive.google.com/drive/folders/17hrzCz8n6e2ZksXkccTjQ2sCA2B9DDRf"),
      ("Computer & Information Science",       "https://drive.google.com/drive/folders/17hrzCz8n6e2ZksXkccTjQ2sCA2B9DDRf"),
      ("Software Engineering",                  "https://drive.google.com/drive/folders/18_gHum3hc9NZlr0NcEOzLhrHQTsZVcPF"),
      ("Cyber Security",                        "https://drive.google.com/drive/folders/18UKInWRHVNB8vR47LtpEQA7oQdQfswwJ"),
      ("Information Technology",                "https://drive.google.com/drive/folders/1wp0bdl-V3GjGhNhiuR2FwWkXmXpMJRIE"),
      ("Information Systems",                   "https://drive.google.com/drive/folders/1z3aGsK0iLJZOuqUj8uBVOjLp2jf_DrHa"),
      ("Computer Science with Electronics",     "https://drive.google.com/drive/folders/1UyTnT9ieBwDUzMiub5PLx6YzbBYoS0Fx"),
      ("Computer Science with Economics",       "https://drive.google.com/drive/folders/1-tUGl0LI-lda0jHtszDthahKJO3jVjUu"),
      ("Forensic Science",                      "https://drive.google.com/drive/folders/10_4vgzL7fq5GNUEHNuMRRaHfe8EntrS4"),
      ("Microbiology",                          "https://drive.google.com/drive/folders/1zFPlsKJo57SU7-0aykJYCGxYd4dJeU5M"),
      ("Biology",                               "https://drive.google.com/drive/folders/1z0qljymGae8Sa2796_U3LQems-FoA1za"),
      ("Chemistry",                             "https://drive.google.com/drive/folders/1uViW7Z43ArYgFXuQxdccm6SrbPClukk6"),
      ("Physics",                               "https://drive.google.com/drive/folders/1c68igR5hODqKuQC1QZfE1Yx4nEmJV4at"),
      ("Physics with Electronics",              "https://drive.google.com/drive/folders/1FXM5FtndbHAiW-T0rDo_Gmi8SaD1IkeD"),
      ("Science Laboratory Technology",         "https://drive.google.com/drive/folders/1twYtraHdOpl4d-rv0hgbWsmhMQn0sUk4"),
      ("Environmental Management & Toxicology", "https://drive.google.com/drive/folders/1dc42_DL9nt_Jp4Z3ESviU-D2Gw_J9EZJ"),
    ]
  },
  {
    "name": "Faculty of Engineering", "abbr": "FENG", "emoji": "⚙️",
    "degree": "B.Eng", "color": "#d97706", "order": 2,
    "drive_url": "https://drive.google.com/drive/folders/1peMRXqufqmXVvxfu0FcuspV002ttO4-R",
    "description": "Engineering students — past papers, lab reports and lecture slides, organised by department.",
    "departments": [
      ("Civil Engineering",                    "https://drive.google.com/drive/folders/1tVPRURvx6N7IHmH1dg_KaGaVLRPeErMA"),
      ("Mechanical Engineering",               "https://drive.google.com/drive/folders/1eCGLGYbN3WiO_idVML-yioUzt9tOtI6p"),
      ("Electrical & Electronics Engineering", "https://drive.google.com/drive/folders/1D9TlhwDzhJNLQMJyroUwFEEvkYX5j7Qx"),
      ("Computer Engineering",                 "https://drive.google.com/drive/folders/1rabWxWsh5TS6gL9CKV26L_Cf7vzasnws"),
      ("Telecommunications Engineering",       "https://drive.google.com/drive/folders/11USrQKmgKYvRaQnHLSP7NKFfWod8H-D0"),
      ("Wood Products Engineering",            "https://drive.google.com/drive/folders/1-h4G4tgzBz8wKi1tNN1OS-dbDNijANG9"),
    ]
  },
  {
    "name": "Faculty of Law", "abbr": "FLAW", "emoji": "⚖️",
    "degree": "LLB / BLD", "color": "#7c3aed", "order": 3,
    "drive_url": "https://drive.google.com/drive/folders/1OGBD9sh-XuFhVveetCf5nEG11SEFczhb",
    "description": "Law students — case summaries, moots, past bar prep and more, all in one place.",
    "departments": [
      ("Bachelor of Laws (LLB)", "https://drive.google.com/drive/folders/1zfdix8GPE6z6fwGFu0a430ubnOuTSAuk"),
      ("Law & Diplomacy (BLD)",  "https://drive.google.com/drive/folders/1GZQ6C4L9xuPN6MTIg-p0ZwrRB3jBwKaY"),
    ]
  },
  {
    "name": "Management & Social Sciences", "abbr": "MSS", "emoji": "📊",
    "degree": "B.Sc", "color": "#0891b2", "order": 4,
    "drive_url": "https://drive.google.com/drive/folders/1QgdipQrXF8v_1jDpqBqcmsE8qE0m53gE",
    "description": "Business, Economics or Social Sciences? Your notes, past questions and textbooks are here.",
    "departments": [
      ("Accounting",                             "https://drive.google.com/drive/folders/12CRp3_XeyWVEHlJ1i5HPE57qu6GCw6GX"),
      ("Business Administration",                "https://drive.google.com/drive/folders/1ZrLCkI2wRDvCEz1ue4WVG_1ydHP8KHC9"),
      ("Economics & Development Studies",        "https://drive.google.com/drive/folders/1HEIO0haAu5UWqjKQYHpYK-w-cMQSx2iw"),
      ("Banking & Finance",                      "https://drive.google.com/drive/folders/1fNgLqDkvkPOzzY5hW1cz55fP9RGQoQQW"),
      ("Entrepreneurship",                       "https://drive.google.com/drive/folders/1A6wTu3_G42WSXQVjKuVbDKS5ly-BD7YZ"),
      ("Industrial Relations & Human Resources", "https://drive.google.com/drive/folders/10JREozQoaHu-GPjDvZBgRGtoFFx9si63"),
      ("Marketing",                              "https://drive.google.com/drive/folders/1bV0APyZTOz45ejV0p8nM9bk43w7mnasV"),
      ("Public Administration",                  "https://drive.google.com/drive/folders/1GahStSjWy7pqfl3f6eyQMT-njqloNvjZ"),
      ("Sociology",                              "https://drive.google.com/drive/folders/145HaFpHhJ2v2tUotnsNPpE7NR0GysohP"),
      ("Psychology",                             "https://drive.google.com/drive/folders/1qcKn3lKoY3_rTgUQey5FKM6mseayA8yb"),
      ("Politics & International Relations",     "https://drive.google.com/drive/folders/1sdHspp42ec8VcW27ofkOOA-yCBS_o0Gd"),
      ("Criminology & Security Studies",         "https://drive.google.com/drive/folders/19Rr-aIQAUF-dP_gALGd1euodauH-pyeX"),
      ("Social Work",                            "https://drive.google.com/drive/folders/1sSaCECfsdBZi1Iypt8Z6SQncveSOSolD"),
      ("Tourism & Hospitality Management",       "https://drive.google.com/drive/folders/1hwrVggAz0aSYgydDzwueRd4ophsxzPcQ"),
    ]
  },
  {
    "name": "Information & Communication Sciences", "abbr": "ICS", "emoji": "📡",
    "degree": "B.Sc", "color": "#db2777", "order": 5,
    "drive_url": "https://drive.google.com/drive/folders/1G_iwGwMMlxELrsDx90aHt400_gEbiqm-",
    "description": "Mass Comm, Media or Library students — past questions and study materials right here.",
    "departments": [
      ("Mass Communication & Media Technology",  "https://drive.google.com/drive/folders/1DEZEtkvXl2KrTKpZB1sT4Se3BUY00-bx"),
      ("Journalism",                             "https://drive.google.com/drive/folders/12FdWl0O7krEIDOSX3j8MlnYHLH3LoSnq"),
      ("Public Relations",                       "https://drive.google.com/drive/folders/1ZlldvAW2eLjszoq4JVYiAH2-qdxGnZvr"),
      ("Advertising",                            "https://drive.google.com/drive/folders/1TUdPy-QO_i7RI578Rr-1nCuY7W5xBr6f"),
      ("Media Studies",                          "https://drive.google.com/drive/folders/1v2YCUeZLv6C8tLWDtPvc8kv45QoHVmrA"),
      ("Information Science & Media Studies",    "https://drive.google.com/drive/folders/1Wql05pnVaQJoZh3f_3ithhWNWWo7lmlk"),
      ("Library, Archival & Information Studies","https://drive.google.com/drive/folders/1vG3OzaW6MoqDDOjiFdOmN4gZ2Lu-72HZ"),
      ("Office and Information Management",      "https://drive.google.com/drive/folders/18GsPEMMq3fQazdUmE2K2ruoE_FD1iPwy"),
      ("Printing and Publishing",                "https://drive.google.com/drive/folders/1FCGVg-2zLLDB8utVnuhygLMNUKOCdNFG"),
      ("Health Information Management",          "https://drive.google.com/drive/folders/1ngxTDQU7pROLKMQjfO-rnfUva3jgVRf6"),
    ]
  },
  {
    "name": "Environmental Design", "abbr": "FEDM", "emoji": "🏗️",
    "degree": "B.Sc / B.Arch", "color": "#ea580c", "order": 6,
    "drive_url": "https://drive.google.com/drive/folders/1-jczQm9rH9dxMPnsww5p-Y7PoBDoEDsc",
    "description": "Architecture and Planning students — design briefs, notes and past questions all in one place.",
    "departments": [
      ("Architecture",                 "https://drive.google.com/drive/folders/16pp00W_LXsu9LEJvSmu09aLjh1pBdSFO"),
      ("Urban and Regional Planning",  "https://drive.google.com/drive/folders/1xrsdrDz3JKFITzhOsGdJKgGn3valt-8p"),
      ("Building",                     "https://drive.google.com/drive/folders/1TFzfdXhrc85dio2XnTlI_fL-rXIMXn6g"),
      ("Estate Management",            "https://drive.google.com/drive/folders/1OBavcUcGeZ_js9VHEfbnnCx4Eu-8YIAv"),
      ("Quantity Surveying",           "https://drive.google.com/drive/folders/16S8bdkGDz3QOYSgu0xhSHIUfFrIoT9qU"),
      ("Surveying and Geoinformatics", "https://drive.google.com/drive/folders/146OtBUVafkK1G-gCUWluH1uXPXZxIiJl"),
    ]
  },
  {
    "name": "Faculty of Arts", "abbr": "FARTS", "emoji": "📚",
    "degree": "B.A", "color": "#9333ea", "order": 7,
    "drive_url": "https://drive.google.com/drive/folders/1RP2EpTZ_5ChHuCF5yrnGl2PHol8Uzwr-",
    "description": "Languages, Literature or Performing Arts — find all your study materials here.",
    "departments": [
      ("English & Literary Studies",     "https://drive.google.com/drive/folders/1ScghG5cNsiSBIPR8O6Feyi_vWzXeNRFc"),
      ("Performing Arts & Film Studies", "https://drive.google.com/drive/folders/1kfkbMRBsnEFKJqqHV9iRbdFGbTa-lvH9"),
      ("Religious Studies",              "https://drive.google.com/drive/folders/1cJCFsSpW0Yt1f1BhVlTHeneBJdZS8nlc"),
    ]
  },
  {
    "name": "Faculty of Education", "abbr": "FEDU", "emoji": "🎓",
    "degree": "B.Ed", "color": "#0d9488", "order": 8,
    "drive_url": "https://drive.google.com/drive/folders/1O2IYhKUaeT7ErhER_nyWYJsuAstPJ1-1",
    "description": "Education students — past questions, lesson plans and study resources, sorted by department.",
    "departments": [
      ("Biology Education",           "https://drive.google.com/drive/folders/1W-zUBkboKYhXYzjvxcNU1Ga3PdLAN6bZ"),
      ("Chemistry Education",         "https://drive.google.com/drive/folders/1zDh-_DkoAzrcSYfV7JWP6-O4Qnx5ck5_"),
      ("Physics Education",           "https://drive.google.com/drive/folders/14cpYWFliNIsyEA0LSEdpFG8NCFOZJLgd"),
      ("Computer Science Education",  "https://drive.google.com/drive/folders/1oy04CxDgujisWh9zma-hQNP-BV87fBwC"),
      ("Mathematics Education",       "https://drive.google.com/drive/folders/1aa2XRl1LFZOC5H6wOJjnxtB3JKob37iD"),
      ("English Education",           "https://drive.google.com/drive/folders/1LLZu_X6cV7DfWV-0Lyok47y9tSHKcr1m"),
      ("Social Studies Education",    "https://drive.google.com/drive/folders/1su5I5avcc-BYz4HYTjzPT2oFVDolvEMV"),
      ("Business Studies Education",  "https://drive.google.com/drive/folders/1G35s4ujK2W94xlVMGPD8J8L7nbSnqVUw"),
      ("Physical & Health Education", "https://drive.google.com/drive/folders/1nfdGORBvsa2VbdTGP5L6g_SEsznTHzoA"),
      ("Educational Management",      "https://drive.google.com/drive/folders/1q9SoNNZj8hk_hlYteCVpP_WF-EnMqR3T"),
    ]
  },
  {
    "name": "College of Medicine", "abbr": "COM", "emoji": "🩺",
    "degree": "MBBS / B.Sc", "color": "#dc2626", "order": 9,
    "drive_url": "https://drive.google.com/drive/folders/1rTuz1ZLGiE-mudSJdAnLhfrpN0ScnJrA",
    "description": "Medical and health science students — anatomy notes, past questions and clinical resources, organised for you.",
    "departments": [
      ("Medicine",                            "https://drive.google.com/drive/folders/1mOPTCIs_u5cZEqW3sqWHuwdG9bTTs5lU"),
      ("Dentistry",                           "https://drive.google.com/drive/folders/1KVZ7d9sIf6xe6IQY9Odzg6rjgy-gnVA1"),
      ("Nursing",                             "https://drive.google.com/drive/folders/1uglw8uhyRiyt2o46aDHDrk-04cejhAY9"),
      ("Physiotherapy",                       "https://drive.google.com/drive/folders/1WnWjdx8a42ImNS4inn-EEey5rljuaJvL"),
      ("Medical Laboratory Science",          "https://drive.google.com/drive/folders/1AeHkYEHm_I-rhGEsY_yU1cKrOGqFlHGC"),
      ("Medical Radiography",                 "https://drive.google.com/drive/folders/1EhoxmvnQUXB994ct_OL7I0n32TcuHtQ_"),
      ("Human Anatomy",                       "https://drive.google.com/drive/folders/1LAtoiIn_8ZyrvkGcmTRufLnb9Y5R_SdQ"),
      ("Physiology",                          "https://drive.google.com/drive/folders/1k17D0mKSRu70IgFWvXTIdccjL0GoVXpb"),
      ("Biochemistry",                        "https://drive.google.com/drive/folders/1OsWpKY12FUobPlD4__CZHZKx_o4gvPLb"),
      ("Pharmacology",                        "https://drive.google.com/drive/folders/13tlo5R071nJPccBryyPVFIdt4hhPPRMy"),
      ("Medical Microbiology & Parasitology", "https://drive.google.com/drive/folders/16VFK4KmZvoC6mM7XbzOsMf4KWGmEdlnW"),
      ("Community Health",                    "https://drive.google.com/drive/folders/1su_3sczAi8baIUm87T8sXL_RYdwpR4Gi"),
      ("Human Nutrition & Dietetics",         "https://drive.google.com/drive/folders/12drmc8Op7uhubL-cfSQ9jR9sK8Iw77Sk"),
      ("Environmental Health Sciences",       "https://drive.google.com/drive/folders/1RrIEKCj_6cgT11fUzET3NMjcfMUKJ5Od"),
      ("Health Policy & Management",          "https://drive.google.com/drive/folders/1dDo-r6C3gu-MnXDCtJPzrepRztN23Ma-"),
      ("Preventive Medicine & Primary Care",  "https://drive.google.com/drive/folders/1MyIafUv_fn_Krc_GPxI7p-WvWROl__f1"),
      ("Health Information Management",       "https://drive.google.com/drive/folders/1FZyvZscClkxfjmyYNOqUM8ikNAO1q-1A"),
      ("Health Promotion & Education",        "https://drive.google.com/drive/folders/17JtaPPNwTNYcWc9JS2IStnMQQQMTpYPo"),
    ]
  },
  {
    "name": "Faculty of Pharmacy", "abbr": "FPHARM", "emoji": "💊",
    "degree": "Pharm.D", "color": "#0891b2", "order": 10,
    "drive_url": "https://drive.google.com/drive/folders/1R8PFt-3VvLe2HJmPo2_44A2r-grpiw6M",
    "description": "Pharmacy students — drug notes, past questions and clinical study materials right here.",
    "departments": [
      ("Pharmacy (Doctor of Pharmacy - Pharm.D)", "https://drive.google.com/drive/folders/10kxbnCjnMFwDbV5I_yClD77jcUP47skF"),
    ]
  },
]


class Command(BaseCommand):
    help = "Seed all 10 LCU faculties and 85 departments into the database"

    def handle(self, *args, **kwargs):
        created_f = created_d = skipped = 0

        for f_data in FACULTY_DATA:
            faculty, f_new = Faculty.objects.update_or_create(
                slug=slugify(f_data["name"]),
                defaults={
                    "name":        f_data["name"],
                    "abbr":        f_data["abbr"],
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
                self.stdout.write(f"  ✅ Faculty: {faculty.name}")
            else:
                self.stdout.write(f"  ↻  Updated: {faculty.name}")

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
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Done — {created_f} faculties, {created_d} new departments "
            f"({skipped} already existed / updated)"
        ))
