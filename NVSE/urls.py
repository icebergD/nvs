from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('mainapp.urls')),
    path('table/', include('tableapp.urls')),
    path('api/', include('apiapp.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('excel/', include('excel_table.urls')),
]
