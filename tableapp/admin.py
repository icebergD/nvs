from django.contrib import admin

from .models import Table1, Field1, FieldExcel1, ValueChar1, ValueInt1, ValueFloat1, Permision1

admin.site.register(Table1)
admin.site.register(Permision1)
admin.site.register(Field1)
admin.site.register(FieldExcel1)
admin.site.register(ValueChar1)
admin.site.register(ValueInt1)
admin.site.register(ValueFloat1)
