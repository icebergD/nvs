from django.urls import path
from . import views

urlpatterns = [
    path('users-list', views.UsersList.as_view(), name='users-list'),
    path('delite-user', views.DeliteUser.as_view(), name='delite-user'),
    path('user-add', views.AddUser.as_view(), name='user-add'),
    # path('user-add', views.register, name='user-add'),
    path('change-password', views.ChangePassword.as_view(), name='change-password'),
]
