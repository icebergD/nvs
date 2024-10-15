from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello, name='hello'),
    path('', views.Home.as_view(), name='home'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('form-constructor', views.form_constructor, name='form-constructor'),
    path('create-form', views.create_form, name='create-form'),

    path('one-line-table-list', views.OneLineTableList.as_view(), name='one-line-table-list'),
    path('one-line-table-generator', views.OneLineTableGenerator.as_view(), name='one-line-table-generator'),
    path('one-line-table-show', views.OneLineTableShow.as_view(), name='one-line-table-show'),

    path('one-line-table-copy', views.OneLineTableCopy.as_view(), name='one-line-table-copy'),
    path('one-line-table-edit', views.OneLineTableEdit.as_view(), name='one-line-table-edit'),
    path('one-line-table-toggle-visable', views.OneLineTableToggleVisable.as_view(), name='one-line-table-toggle-visable'),

    path('configure-table', views.configure_table.as_view(), name='configure-table'),
    path('open-table', views.open_table.as_view(), name='open-table'),
    path('delite-table', views.delite_table.as_view(), name='delite-table'),

    path('client-home', views.client_home.as_view(), name='client-home'),
    path('client-fill/<int:permision_id>/', views.client_fill.as_view(), name='client-fill'),
    path('client-send', views.client_send.as_view(), name='client-send'),

    path('test', views.test.as_view())

]
