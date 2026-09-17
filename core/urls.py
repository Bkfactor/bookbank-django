from django.urls import path
from . import views

urlpatterns = [
    path("",                          views.home,            name="home"),
    path("faculty/<slug:slug>/",      views.faculty_detail,  name="faculty"),
    path("search/",                   views.search,          name="search"),
    path("upload/",                   views.upload,          name="upload"),
    path("upload/success/",           views.upload_success,  name="upload_success"),
    path("review/<int:resource_id>/", views.submit_review,   name="submit_review"),
    path("rating/<int:resource_id>/", views.submit_rating,   name="submit_rating"),
    path("feedback/",                 views.feedback_view,   name="submit_feedback"),
    path("ajax/departments/",         views.load_departments, name="load_departments"),
    path("tools/",                    views.tools_hub,       name="tools_hub"),
    path("tools/cgpa-calculator/",    views.cgpa_calculator, name="cgpa_calculator"),
    path("tools/target-cgpa/",        views.target_cgpa,     name="target_cgpa"),
    path("tools/citation-generator/", views.citation_generator, name="citation_generator"),
    path("tools/flashcards/",         views.flashcards,      name="flashcards"),
    path("tools/exam-tracker/",       views.exam_tracker,    name="exam_tracker"),
]
