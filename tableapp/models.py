from django.db import models

from django.conf import settings


class Table1(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name='Жадвал номи')
    description = models.TextField(verbose_name='Жадвал тавсифи', null=True, blank=True)
    width = models.IntegerField(verbose_name='ширина', null=True, blank=True)
    height = models.IntegerField(verbose_name='высота', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class Permision1(models.Model):
    table_created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='table_created_user')
    table = models.ForeignKey(Table1, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finished = models.DateTimeField(null=True, blank=True)
    coord_x = models.IntegerField(verbose_name='столбик', null=True, blank=True)
    coord_y = models.IntegerField(verbose_name='строка', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.user.first_name

class FieldExcel1(models.Model):
    table = models.ForeignKey(Table1, on_delete=models.CASCADE)
    coord_x = models.IntegerField(verbose_name='столбик', null=True, blank=True)
    coord_y = models.IntegerField(verbose_name='строка', null=True, blank=True)
    value = models.CharField(max_length=250, verbose_name='значение', null=True, blank=True)
    colspan = models.IntegerField(verbose_name='длина ячейки', null=True, blank=True)


class Field1(models.Model):
    table = models.ForeignKey(Table1, on_delete=models.CASCADE)
    coord_x = models.IntegerField(verbose_name='столбик', null=True, blank=True)
    coord_y = models.IntegerField(verbose_name='строка', null=True, blank=True)
    name = models.CharField(max_length=250, verbose_name='майдон номи')
    description = models.TextField(verbose_name='Тавсифи', null=True, blank=True)
    f_type = models.CharField(max_length=1, verbose_name='майдон тури', null=True, blank=True)#t-text, i-int, f-float
    required = models.BooleanField(default=False, verbose_name='шарт ми')

    def __str__(self):
        return self.name

class ValueChar1(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field = models.ForeignKey(Field1, on_delete=models.CASCADE, verbose_name='майдон номи')
    value = models.CharField(max_length=250, verbose_name='майдон қиймати', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name}, {self.field.name}, {self.value}'

class ValueInt1(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field = models.ForeignKey(Field1, on_delete=models.CASCADE, verbose_name='майдон номи')
    value = models.IntegerField(verbose_name='майдон қиймати', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name}, {self.field.name}, {self.value}'

class ValueFloat1(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field = models.ForeignKey(Field1, on_delete=models.CASCADE, verbose_name='майдон номи')
    value = models.DecimalField( max_digits=10, decimal_places=2, verbose_name='майдон қиймати', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name}, {self.field.name}, {self.value}'