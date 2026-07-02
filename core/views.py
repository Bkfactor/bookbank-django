from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.http import JsonResponse
from .models import Faculty, Department, Resource, Review
from .forms import SubmitResourceForm, ReviewForm


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
        form = SubmitResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("upload_success")
    else:
        form = SubmitResourceForm()

    faculties = Faculty.objects.prefetch_related("departments").all()
    return render(request, "core/upload.html", {
        "form": form,
        "faculties": faculties,
    })


def upload_success(request):
    return render(request, "core/upload_success.html")


def submit_review(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id, status="approved")
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.resource = resource
            review.save()
            return JsonResponse({"ok": True,
                                 "avg": resource.avg_rating(),
                                 "count": resource.review_count()})
    return JsonResponse({"ok": False}, status=400)


def load_departments(request):
    """AJAX: return departments for a faculty (for the upload form dropdown)."""
    faculty_id = request.GET.get("faculty_id")
    departments = Department.objects.filter(faculty_id=faculty_id)\
                                    .values("id", "name")
    return JsonResponse(list(departments), safe=False)
