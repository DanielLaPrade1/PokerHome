from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import NewUserForm


def RegisterView(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = NewUserForm()
    return render(request, 'authentication/register.html', {"form": form})
