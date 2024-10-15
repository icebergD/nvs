from django.urls import path
from . import views

urlpatterns = [
    path('one-table-list', views.OneTableList.as_view(), name='one-table-list'),
    path('one-table-generator', views.OneTableGenerator.as_view(), name='one-table-generator'),
    path('one-table-show', views.OneTableShow.as_view(), name='one-table-show'),
    path('one-table-edit', views.OneTableEdit.as_view(), name='one-table-edit'),
    path('one-table-delite', views.OneTableDelite.as_view(), name='one-table-delite'),
]
