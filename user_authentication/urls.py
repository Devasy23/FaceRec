from django.urls import path

from .views import profile, register, user_login

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("profile/", profile, name="profile"),
]
