from .models import Faculty, Resource


def site_stats(request):
    """Injects material/faculty/dept counts into every template automatically."""
    return {
        "total_materials": Resource.objects.filter(status="approved").count(),
        "total_faculties": Faculty.objects.count(),
        "total_depts": sum(f.dept_count() for f in Faculty.objects.all()),
    }
