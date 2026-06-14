
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy

from .views import EditUserView, RegisterView, UserDetailView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="core:home"), name="logout"),
    path("profile/edit/", EditUserView.as_view(), name="edit_profile"),
    path("profile/details/", UserDetailView.as_view(), name="user_details"),
    path(
        "profile/password/",
        PasswordChangeView.as_view(
            template_name="users/change_password.html",
            success_url=reverse_lazy("core:home"),
        ),
        name="change_password",
    ),
]