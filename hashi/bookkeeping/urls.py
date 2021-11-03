from bookkeeping import views
from django.urls import path

app_name = "bookkeeping"

urlpatterns = [
    path("", views.entry_list, name="entry-list"),
]
