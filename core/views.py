from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.http import JsonResponse
from .models import Faculty, Department, Resource, Review, Rating, Feedback
from .forms import SubmitResourceForm, ReviewForm, FeedbackForm
import cloudinary.uploader

def home(request):
    faculties = Faculty.objects.prefetch_related("departments").all()
    recent    = Resource.objects.filter(status="approved")\
                        .select_related("faculty", "department")\
                        .order_by("-published_at")[:6]
    return render(request, "core/index.html", {
        "faculties": faculties,
        "recent":    recent,
    })


def faculty_detail(request, slug):
    faculty = get_object_or_404(
        Faculty.objects.prefetch_related("departments"), slug=slug
    )
    departments = faculty.departments.all()

    # Which department tab is active?
    dept_slug = request.GET.get("dept")
    if dept_slug:
        active_dept = get_object_or_404(Department, faculty=faculty, slug=dept_slug)
    else:
        active_dept = departments.first()

    materials = Resource.objects.filter(
        department=active_dept, status="approved"
    ).order_by("-published_at") if active_dept else []

    return render(request, "core/faculty.html", {
        "faculty":     faculty,
        "departments": departments,
        "active_dept": active_dept,
        "materials":   materials,
    })


def search(request):
    q     = request.GET.get("q", "").strip()
    level = request.GET.get("level", "").strip()
    type_ = request.GET.get("type", "").strip()

    results = Resource.objects.filter(status="approved")\
                              .select_related("faculty", "department")

    if q:
        results = results.filter(
            Q(title__icontains=q)           |
            Q(department__name__icontains=q)|
            Q(faculty__name__icontains=q)   |
            Q(uploaded_by__icontains=q)
        )
    if level:
        results = results.filter(level=level)
    if type_:
        results = results.filter(type=type_)

    results = results.order_by("-published_at")

    return render(request, "core/search.html", {
        "results": results,
        "q":       q,
        "level":   level,
        "type":    type_,
        "type_choices": Resource.TYPE_CHOICES,
    })


def upload(request):
    if request.method == "POST":
        form = SubmitResourceForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            uploaded_file = request.FILES.get("file")
            if uploaded_file:
                result = cloudinary.uploader.upload(
                    uploaded_file,
                    resource_type="raw",
                    folder="bookbank/materials",
                )
                instance.file_url = result.get("secure_url", "")
            instance.uploaded_by = form.cleaned_data.get("name", "Anonymous")
            instance.contact = form.cleaned_data.get("contact", "")
            instance.status = "pending"
            instance.save()
            return redirect("upload_success")
    else:
        form = SubmitResourceForm()
    return render(request, "core/upload.html", {"form": form})


def upload_success(request):
    return render(request, "core/upload_success.html")


def submit_rating(request, resource_id):
    if request.method == "POST":
        resource = get_object_or_404(Resource, id=resource_id, status="approved")
        try:
            rating_val = int(request.POST.get("rating"))
            if rating_val < 1 or rating_val > 5:
                return JsonResponse({"ok": False}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({"ok": False}, status=400)
            
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        
        Rating.objects.update_or_create(
            resource=resource,
            session_key=session_key,
            defaults={"rating": rating_val}
        )
        return JsonResponse({"ok": True, "avg": resource.avg_rating()})
    return JsonResponse({"ok": False}, status=400)

def submit_review(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id, status="approved")
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.resource = resource
            review.status = "pending"
            review.save()
            return JsonResponse({"ok": True, "msg": "Review submitted and is awaiting moderation."})
    return JsonResponse({"ok": False}, status=400)

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "core/feedback_success.html")
    else:
        form = FeedbackForm()
    return render(request, "core/feedback.html", {"form": form})

def load_departments(request):
    """AJAX: return departments for a faculty (for the upload form dropdown)."""
    faculty_id = request.GET.get("faculty_id")
    departments = Department.objects.filter(faculty_id=faculty_id)\
                                    .values("id", "name")
    return JsonResponse(list(departments), safe=False)


def tools_hub(request):
    """Hub page for all student tools."""
    return render(request, "core/tools_hub.html")


def cgpa_calculator(request):
    """A completely client-side CGPA calculator. No data saved."""
    return render(request, "core/cgpa_calculator.html")


def target_cgpa(request):
    """A completely client-side Target CGPA calculator."""
    return render(request, "core/target_cgpa.html")


def citation_generator(request):
    """A client-side APA Citation Generator."""
    return render(request, "core/citation_generator.html")


def flashcards(request):
    """A client-side Flashcard/Quiz tool using localStorage."""
    return render(request, "core/flashcards.html")


def exam_tracker(request):
    """A client-side Exam Tracker with Notifications using localStorage."""
    return render(request, "core/exam_tracker.html")


def study_hub(request):
    """A Pomodoro timer and ambient sound player."""
    return render(request, "core/study_hub.html")
