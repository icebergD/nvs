
# from .views import excel_table_view
#
# urlpatterns = [
#     path('', excel_table_view, name='excel_table'),
# ]

from django.urls import path
from . import views

# app_name = 'viewer'

urlpatterns = [
    path('excel-table-list/', views.ExcelTableList.as_view(), name='excel-table-list'),

    path('excel-table-toggle-visable', views.ExcelTableToggleVisable.as_view(), name='excel-table-toggle-visable'),
    path('delete-excel-table', views.DeleteExcelTable.as_view(), name='delete-excel-table'),
    path('upload/', views.UploadExcel.as_view(), name='upload_excel'),

    path('configure-excel/<int:pk>/', views.ConfigureExcel.as_view(), name='configure-excel'),
    path('client-excel-table-list', views.ClientExcelTableList.as_view(), name='client-excel-table-list'),
    path('client-excel-fill/<int:pk>/', views.ClientExcelFill.as_view(), name='client-excel-fill'),

    path('excel-table-view/<int:pk>/', views.ExcelTableView.as_view(), name='excel-table-view'),

    path('view/<int:pk>/', views.view_excel, name='view_excel'),
    path('view/<int:pk>/<str:sheet_name>/', views.view_sheet, name='view_sheet'),

]