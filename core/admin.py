from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Faculty, Department, Resource, Review, Rating, Feedback
from unfold.admin import ModelAdmin, TabularInline

class DepartmentInline(TabularInline):
    model   = Department
    extra   = 1
    fields  = ("name", "slug", "drive_url", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Faculty)
class FacultyAdmin(ModelAdmin):
    list_display  = ("emoji", "abbr", "name", "degree", "dept_count", "material_count", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    inlines       = [DepartmentInline]
    search_fields = ("name", "abbr")

    def dept_count(self, obj):
        return obj.dept_count()
    dept_count.short_description = "Depts"

    def material_count(self, obj):
        return obj.material_count()
    material_count.short_description = "Materials"


@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display  = ("name", "faculty", "material_count", "drive_url")
    list_filter   = ("faculty",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def material_count(self, obj):
        return obj.material_count()
    material_count.short_description = "Materials"


@admin.register(Resource)
class ResourceAdmin(ModelAdmin):
    list_display  = (
        "title", "type_badge", "faculty", "department",
        "level", "status_badge", "avg_rating_display",
        "uploaded_by", "created_at"
    )
    list_filter   = ("status", "type", "faculty", "level")
    list_editable = ()
    search_fields = ("title", "uploaded_by", "contact")
    readonly_fields = ("created_at", "published_at", "drive_link_preview")
    fieldsets = (
        ("Material Info", {
            "fields": ("title", "type", "faculty", "department", "level", "year")
        }),
        ("Drive Link", {
            "fields": ("file_url", "drive_url", "drive_link_preview")
        }),
        ("Submission", {
            "fields": ("uploaded_by", "contact", "created_at")
        }),
        ("Review & Publishing", {
            "fields": ("status", "admin_note", "published_at")
        }),
    )
    actions = ["approve_selected", "reject_selected"]

    def type_badge(self, obj):
        colors = {
            "past-questions": "#fef3c7",
            "lecture-notes":  "#dbeafe",
            "textbook":       "#dcfce7",
            "slides":         "#fce7f3",
            "lab-manual":     "#e0e7ff",
            "outline":        "#f3f4f6",
        }
        bg = colors.get(obj.type, "#f3f4f6")
        return format_html(
            '<span style="background:{};padding:2px 8px;border-radius:4px;'
            'font-size:12px;font-weight:600;color:#1f2937">{}</span>',
            bg, obj.get_type_display()
        )
    type_badge.short_description = "Type"

    def status_badge(self, obj):
        colors = {
            "pending":  ("#fef3c7", "#92400e"),
            "approved": ("#dcfce7", "#166534"),
            "rejected": ("#fee2e2", "#991b1b"),
        }
        bg, fg = colors.get(obj.status, ("#f3f4f6", "#374151"))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:4px;font-size:12px;font-weight:600;">{}</span>',
            bg, fg, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def avg_rating_display(self, obj):
        avg = obj.avg_rating()
        if avg is None:
            return "—"
        return f"⭐ {avg} ({obj.review_count()} reviews)"
    avg_rating_display.short_description = "Rating"

    def drive_link_preview(self, obj):
        if obj.drive_url:
            return format_html(
                '<a href="{}" target="_blank" style="color:#1d4ed8;">'
                '🔗 Open in Google Drive</a>', obj.drive_url
            )
        return "—"
    drive_link_preview.short_description = "Drive Preview"

    def approve_selected(self, request, queryset):
        updated = queryset.update(status="approved", published_at=timezone.now())
        self.message_user(request, f"{updated} resource(s) approved and now live.")
    approve_selected.short_description = "✅ Approve selected resources"

    def reject_selected(self, request, queryset):
        updated = queryset.update(status="rejected")
        self.message_user(request, f"{updated} resource(s) rejected.")
    reject_selected.short_description = "❌ Reject selected resources"

    def save_model(self, request, obj, form, change):
        if obj.status == "approved" and not obj.published_at:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("resource", "reviewer_name", "comment_preview", "status_badge", "created_at")
    list_filter  = ("status",)
    search_fields = ("reviewer_name", "comment", "resource__title")
    actions = ["approve_selected", "reject_selected"]

    def comment_preview(self, obj):
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = "Comment"

    def status_badge(self, obj):
        colors = {
            "pending":  ("#fef3c7", "#92400e"),
            "approved": ("#dcfce7", "#166534"),
            "rejected": ("#fee2e2", "#991b1b"),
        }
        bg, fg = colors.get(obj.status, ("#f3f4f6", "#374151"))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:4px;font-size:12px;font-weight:600;">{}</span>',
            bg, fg, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def approve_selected(self, request, queryset):
        updated = queryset.update(status="approved")
        self.message_user(request, f"{updated} review(s) approved.")
    approve_selected.short_description = "✅ Approve selected reviews"

    def reject_selected(self, request, queryset):
        updated = queryset.update(status="rejected")
        self.message_user(request, f"{updated} review(s) rejected.")
    reject_selected.short_description = "❌ Reject selected reviews"


@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    list_display = ("resource", "rating", "created_at")
    list_filter = ("rating",)


@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin):
    list_display = ("name", "category_badge", "status_badge", "created_at")
    list_filter = ("status", "category")
    search_fields = ("name", "email", "message")
    actions = ["mark_in_progress", "mark_resolved"]

    def category_badge(self, obj):
        return obj.get_category_display()
    category_badge.short_description = "Category"

    def status_badge(self, obj):
        colors = {
            "pending":  ("#fef3c7", "#92400e"),
            "in_progress": ("#dbeafe", "#1e40af"),
            "resolved": ("#dcfce7", "#166534"),
        }
        bg, fg = colors.get(obj.status, ("#f3f4f6", "#374151"))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:4px;font-size:12px;font-weight:600;">{}</span>',
            bg, fg, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status="in_progress")
        self.message_user(request, f"{updated} feedback marked as In Progress.")
    mark_in_progress.short_description = "🔄 Mark as In Progress"

    def mark_resolved(self, request, queryset):
        updated = queryset.update(status="resolved")
        self.message_user(request, f"{updated} feedback marked as Resolved.")
    mark_resolved.short_description = "✅ Mark as Resolved"

