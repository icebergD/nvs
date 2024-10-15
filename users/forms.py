from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from django.conf import settings

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('role','first_name',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('role', 'first_name',)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Парол', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Паролни қайтаринг', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Исмингизни киритинг')
    username = forms.CharField(label='Логин')
    # role = forms.ChoiceField(label='Статус')
    first_name.widget.attrs['required'] = 'required'
    password.widget.attrs['class'] = 'form-control'
    password2.widget.attrs['class'] = 'form-control'
    first_name.widget.attrs['class'] = 'form-control'
    username.widget.attrs['class'] = 'form-control'
    # role.widget.attrs['class'] = 'form-select'
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'role')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field=='role':
                self.fields[field].widget.attrs.update({
                    'class': 'form-select'
                })

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']