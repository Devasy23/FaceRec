from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


# Form for user registration
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("role",)  # Add role field
