from django import forms
from .models import Resource, Review, Faculty, Department, Feedback

class SubmitResourceForm(forms.ModelForm):
    """
    The student-facing submission form.
    Status defaults to 'pending' — you approve in admin.
    """
    name = forms.CharField(
        max_length=150,
        label="Your Name",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Leevi Benjamin or Anonymous"})
    )
    contact = forms.EmailField(
        required=False,
        label="Email (optional)",
        widget=forms.EmailInput(attrs={"placeholder": "For follow-up only — not published"})
    )
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        label="Faculty",
        empty_label="— Select Faculty —"
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),  # populated dynamically
        label="Department",
        empty_label="— Select Department —"
    )

    class Meta:
        model  = Resource
        fields = ["title", "type", "faculty", "department",
                  "level", "year", "drive_url"]
        labels = {
            "title":     "Material Title",
            "type":      "Material Type",
            "level":     "Level",
            "year":      "Academic Year (optional)",
            "file_url":  "Upload File (PDF, DOCX, PPTX etc.)",
            "drive_url": "Google Drive Link",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "e.g. GST 107 Past Questions 2023/2024"
            }),
            "year": forms.TextInput(attrs={"placeholder": "e.g. 2023/2024"}),
            "drive_url": forms.URLInput(attrs={
                "placeholder": "https://drive.google.com/..."
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If faculty is already selected (POST), populate department dropdown
        if "faculty" in self.data:
            try:
                faculty_id = int(self.data.get("faculty"))
                self.fields["department"].queryset = Department.objects.filter(
                    faculty_id=faculty_id
                )
            except (ValueError, TypeError):
                pass

        def clean(self):
            cleaned_data = super().clean()

            file_url = cleaned_data.get("file_url")
            drive_url = cleaned_data.get("drive_url")

            if not file_url and not drive_url:
                raise forms.ValidationError(
                "Please upload a file or provide a Google Drive link."
        )

            return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.uploaded_by = self.cleaned_data.get("name", "Anonymous")
        instance.contact     = self.cleaned_data.get("contact", "")
        instance.status      = "pending"
        if commit:
            instance.save()
        return instance


class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ["reviewer_name", "comment"]
        labels = {"reviewer_name": "Your Name", "comment": "Review"}
        widgets = {
            "reviewer_name": forms.TextInput(attrs={"placeholder": "e.g. John Doe or Anonymous"}),
            "comment": forms.Textarea(attrs={"rows": 3,
                "placeholder": "Tell students why this material is useful…"})
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "email", "category", "message"]
        labels = {
            "name": "Your Name",
            "email": "Email Address (optional, for follow-up)",
            "category": "What can we help you with?",
            "message": "Details"
        }
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Please provide details..."}),
        }
