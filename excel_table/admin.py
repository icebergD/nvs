from django.contrib import admin
from .models import ExcelTable, Cell, ExcelTableFinish, CellInput

admin.site.register(ExcelTableFinish)
admin.site.register(ExcelTable)
admin.site.register(Cell)
admin.site.register(CellInput)
