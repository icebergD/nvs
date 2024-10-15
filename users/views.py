from django.contrib.auth.forms import UserCreationForm
# from django.core.checks import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import get_user_model
from django.views.generic import CreateView

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .mixins import UserStatus
from .forms import CustomUserCreationForm, UserRegistrationForm

class UsersList(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 't':#Жадвал ва фойдаланувчи яратувчиси

            User = get_user_model()
            # users_list = User.objects.all().values()
            users_list = User.objects.filter(created_user=request.user).values()
            context = {
                'users_list': users_list,
                'navbar': 'users-list',
                'status': self.m_user,
                'user_name': self.user_name
            }
            return render(request, "users/usersList.html", context=context)
        else:
            return redirect('login')

class DeliteUser(UserStatus, View):
    def post(self, request, *args, **kwargs):
        if self.m_user == 't':#Жадвал ва фойдаланувчи яратувчиси
            id = request.POST.get("val")
            User = get_user_model()
            users_list = User.objects.filter(id=id, created_user=request.user).delete()
            return redirect('users-list')
        else:
            return redirect('login')

class AddUser(UserStatus, View):
    def post(self, request, *args, **kwargs):
        if self.m_user == 't':#Жадвал ва фойдаланувчи яратувчиси
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.created_user = request.user
                new_user.save()
                return redirect('users-list')
        else:
            return redirect('login')
    def get(self, request, *args, **kwargs):
        if self.m_user == 't':#Жадвал ва фойдаланувчи яратувчиси
            user_form = UserRegistrationForm()
            return render(request, 'users/userAdd.html', {'user_form': user_form, 'status': self.m_user})
        else:
            return redirect('login')

class ChangePassword(UserStatus, View):
    def post(self, request, *args, **kwargs):
        if self.m_user != 'a': # Залогиненый пользователь
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('change-password')
            else:
                messages.error(request, 'Please correct the error below.')
                return render(request, 'users/changePassword.html', {
                    'form': form
                })
        else:
            return redirect('login')
    def get(self, request, *args, **kwargs):
        if self.m_user != 'a':# Залогиненый пользователь
            form = PasswordChangeForm(request.user)
            return render(request, 'users/changePassword.html', {
                'form': form,
                'status': self.m_user
            })
            # return render(request, 'users/userAdd.html', {'user_form': user_form, 'status': self.m_user})
        else:
            return redirect('login')
