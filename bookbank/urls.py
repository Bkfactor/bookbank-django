from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customise admin header
admin.site.site_header = "LCU Book Bank · Admin"
admin.site.site_title  = "Book Bank Admin"
admin.site.index_title = "Resource Management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

def get_file_url(self):
    if self.file:
        return self.file.url
    return self.drive_url or ""