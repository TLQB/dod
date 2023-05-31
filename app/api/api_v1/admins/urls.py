# Create your tests here.
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.ListCreateAdminView.as_view(), name="list-create-admin"),
    path(
        "<int:admin_id>/",
        views.DetailEditDeleteAdminView.as_view(),
        name="detail-edit-delete-admin",
    ),
]
