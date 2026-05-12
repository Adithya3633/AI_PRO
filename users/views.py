from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Welcome to your dashboard.")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})
