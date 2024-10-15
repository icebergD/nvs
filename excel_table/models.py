from django.db import models
from django.conf import settings

class CellInput(models.Model):
    value = models.CharField(max_length=100)
    excel_table = models.ForeignKey('ExcelTable', on_delete=models.CASCADE)
    cell_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    row = models.IntegerField()
    col = models.IntegerField()
    sheet = models.IntegerField()
    # cell_type = models.CharField(max_length=1, blank=True, null=True)

class ExcelTableFinish(models.Model):
    table = models.ForeignKey('ExcelTable', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finished = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.table}, {self.user.first_name}, {self.finished}'

class ExcelTable(models.Model):
    file = models.FileField(upload_to=settings.MEDIA_ROOT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Жадвал тавсифи', null=True, blank=True)
    visable = models.BooleanField(verbose_name='Бошқаларга кўринадиган', default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.file.name

class Cell(models.Model):
    excel_table = models.ForeignKey(ExcelTable, on_delete=models.CASCADE)
    cell_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    row = models.IntegerField()
    col = models.IntegerField()
    sheet = models.IntegerField()
    cell_type = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return f'{self.excel_table}, {self.cell_user.first_name}, sheet:{self.sheet}, col:{self.col}, row:{self.row}'



