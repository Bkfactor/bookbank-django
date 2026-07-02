from django.db import models
from django.utils.text import slugify


class Faculty(models.Model):
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    abbr        = models.CharField(max_length=10)
    emoji       = models.CharField(max_length=10, default="📚")
    degree      = models.CharField(max_length=60)          # e.g. "B.Sc"
    description = models.TextField()
    drive_url   = models.URLField(blank=True)
    color       = models.CharField(max_length=7, default="#0c1b33")
    order       = models.PositiveIntegerField(default=0)   # display order

    class Meta:
        verbose_name_plural = "Faculties"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.abbr} — {self.name}"

    def dept_count(self):
        return self.departments.count()

    def material_count(self):
        return Resource.objects.filter(
            department__faculty=self, status="approved"
        ).count()


class Department(models.Model):
    faculty   = models.ForeignKey(Faculty, on_delete=models.CASCADE,
                                   related_name="departments")
    name      = models.CharField(max_length=200)
    slug      = models.SlugField()
    drive_url = models.URLField(blank=True)
    order     = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        unique_together = [["faculty", "slug"]]

    def __str__(self):
        return f"{self.faculty.abbr} · {self.name}"

    def material_count(self):
        return self.resources.filter(status="approved").count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Resource(models.Model):
    TYPE_CHOICES = [
        ("past-questions", "📄 Past Questions"),
        ("lecture-notes",  "📝 Lecture Notes"),
        ("textbook",       "📚 Textbook"),
        ("slides",         "🎞️ Slides"),
        ("lab-manual",     "🧪 Lab Manual / Report"),
        ("outline",        "📋 Course Outline / Syllabus"),
    ]
    STATUS_CHOICES = [
        ("pending",  "⏳ Pending Review"),
        ("approved", "✅ Approved — Live"),
        ("rejected", "❌ Rejected"),
    ]
    LEVEL_CHOICES = [(l, f"{l} Level") for l in [100, 200, 300, 400, 500, 600]]

    title        = models.CharField(max_length=300)
    type         = models.CharField(max_length=20, choices=TYPE_CHOICES)
    faculty      = models.ForeignKey(Faculty, on_delete=models.CASCADE,
                                     related_name="resources")
    department   = models.ForeignKey(Department, on_delete=models.CASCADE,
                                     related_name="resources")
    level        = models.IntegerField(choices=LEVEL_CHOICES)
    year         = models.CharField(max_length=20, blank=True,
                                    help_text="e.g. 2023/2024")
    file = models.FileField(upload_to="materials/", blank=True, null=True,
                        help_text="Upload PDF, DOCX, PPTX etc. (max 20MB)")
    drive_url    = models.URLField(help_text="Google Drive sharing link")
    uploaded_by  = models.CharField(max_length=150,
                                    help_text="Submitter name or 'Anonymous'")
    contact      = models.EmailField(blank=True,
                                     help_text="Optional — for follow-up")
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES,
                                    default="pending")
    admin_note   = models.TextField(blank=True,
                                    help_text="Internal note (not shown to students)")
    created_at   = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def avg_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return None
        total = sum(r.rating for r in reviews)
        return round(total / reviews.count(), 1)

    def review_count(self):
        return self.reviews.count()

    def type_emoji(self):
        emojis = {
            "past-questions": "📄",
            "lecture-notes":  "📝",
            "textbook":       "📚",
            "slides":         "🎞️",
            "lab-manual":     "🧪",
            "outline":        "📋",
        }
        return emojis.get(self.type, "📄")
    def get_file_url(self):
    if self.file:
        return self.file.url
    return self.drive_url or ""


class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)]

    resource   = models.ForeignKey(Resource, on_delete=models.CASCADE,
                                   related_name="reviews")
    rating     = models.IntegerField(choices=RATING_CHOICES)
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}★ on '{self.resource.title}'"
