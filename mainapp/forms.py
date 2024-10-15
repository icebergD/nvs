from django.contrib.auth.forms import AuthenticationForm
from django import forms




class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control form-input', 'placeholder':'example_name'}))
    password = forms.CharField(label='Парол', widget=forms.PasswordInput(attrs={'class': 'form-control form-input','placeholder':'Password'}))
