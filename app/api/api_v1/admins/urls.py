# Create your tests here.
from django.urls import path, include
from . import views


urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("check/", views.CheckLoginView.as_view(), name="refresh-admin"),
    path("", views.ListCreateAdminView.as_view(), name="list-create-admin"),
    path(
        "<int:admin_id>/",
        views.DetailEditDeleteAdminView.as_view(),
        name="detail-edit-delete-admin",
    ),
    path(
        "<str:hash>/",
        views.VerifyMailCreateAdminView.as_view(),
        name="create-admin-verify-email",
    ),
]
