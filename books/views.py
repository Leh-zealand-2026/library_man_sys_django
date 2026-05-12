from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .models import Member


# https://docs.djangoproject.com/en/6.0/topics/auth/default/#built-in-auth-views

def home(request):

    return render(request, "books/home.html")


# member registration.
def register(request):
    # we created RegisterForm in forms.py
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            
            user = form.save()
            Member.objects.create(user=user)

            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "books/register.html", {"form": form})