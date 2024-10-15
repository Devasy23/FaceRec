from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, LoginForm


def is_admin(user):
    return user.role == "admin"


@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "authentication/admin_dashboard.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "authentication/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(
                    request,
                    "authentication/login.html",
                    {"error": "Invalid credentials"},
                )
    else:
        form = LoginForm()
    return render(request, "authentication/login.html", {"form": form})


@login_required
def profile(request):
    return render(request, "authentication/profile.html", {"user": request.user})
