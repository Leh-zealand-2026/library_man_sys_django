from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Using the django authentication system.
# https://docs.djangoproject.com/en/6.0/topics/auth/default/
# includes username, password1, password2, and password validation.
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        # django standard User model.
        model = User

        fields = ["username", "email", "password1", "password2"]