from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Pacita Tianna — Site Admin"
admin.site.site_title = "Pacita Tianna Admin"
admin.site.index_title = "Manage the website"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("content.urls")),
    path("api/", include("shop.urls")),
    path("api/", include("gallery.urls")),
    path("api/", include("orders.urls")),
    path("api/", include("lulu_api.urls")),
    path("api/", include("inbox.urls")),
    path("api/", include("dashboard.urls")),
]