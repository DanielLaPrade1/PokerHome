from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class NewUserForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input-small', 'placeholder': 'First Name'}), max_length=20)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input-small', 'placeholder': 'Last Name'}), max_length=20)
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-input-small', 'placeholder': 'Email'}))
    phone = forms.CharField(validators=[CustomUser.phone_regex], widget=forms.TextInput(
        attrs={'class': 'form-input-small', 'placeholder': 'Phone'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Retype Password'}))

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "username",
                  "email", "phone", "password1", "password2")
