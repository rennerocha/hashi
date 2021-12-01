from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bookkeeping/", include("bookkeeping.urls", namespace="bookkeeping")),
    path("django-rq/", include("django_rq.urls")),
    path("webhooks/", include("webhooks.urls", namespace="webhooks")),
]
