from django.contrib import admin

from .models import Table, Field, FieldExcel, ValueChar, ValueInt, ValueFloat, Permision

admin.site.register(Table)
admin.site.register(Permision)
admin.site.register(Field)
admin.site.register(FieldExcel)
admin.site.register(ValueChar)
admin.site.register(ValueInt)
admin.site.register(ValueFloat)