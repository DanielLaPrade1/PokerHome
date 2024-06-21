from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import NewUserForm


def RegisterView(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            # If you want to log the user in and redirect to a new page:
            # login(request, user)
            # redirect to the desired page
            return redirect(reverse('login'))  # Redirect them to login page
    else:
        form = NewUserForm()
    return render(request, 'authentication/register.html', {"form": form})
