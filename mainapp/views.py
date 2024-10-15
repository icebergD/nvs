from django.views.generic import View
from django.http import HttpResponse
from django.http import JsonResponse
import json
import io
from datetime import datetime, timezone
from slugify import slugify

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model
from .models import Table, Field, FieldExcel, Permision, ValueChar, ValueInt, ValueFloat
from .forms import LoginUserForm
from users.mixins import UserStatus

import xlsxwriter


def hello(request):
    return HttpResponse("Hello Medoed")

class Home(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user != 'a':#all besides ananimus

            return render(request, "base.html", {'navbar': 'home', 'status': self.m_user, 'user_name': self.user_name})
        else:
            return redirect('login')

class OneLineTableList(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table = list(Table.objects.filter(user=request.user).order_by('-created').values())
            table_data = []

            for i in table:
                permision = Permision.objects.filter(table__id=i['id'])
                permision_count = len(permision)
                permision_selected = Permision.objects.filter(table__id=i['id'], finished=None)
                permision_selected_count = len(permision_selected)
                if permision_selected_count == 0 and permision_count != 0:
                    color = 'bg-success'
                elif permision_count == 0:
                    color = 'bg-danger'
                else:
                    color = 'bg-danger'
                checked_str = ''
                if i['visable']==True:
                    checked_str = 'checked'
                table_el = {
                    'id': i['id'],
                    'name': i['name'],
                    'description': i['description'],
                    'status': f'{permision_count - permision_selected_count}/{permision_count}',
                    'status_color': color,
                    'checked': checked_str,
                    'created': i['created']
                }
                table_data.append(table_el)
            # print(table_data)
            return render(request, "mainapp/tablesList.html", {'table': table_data, 'navbar': 'one-line-table-list', 'status':self.m_user, 'user_name': self.user_name})
        else:
            return redirect('login')

class OneLineTableGenerator(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            permision = Permision.objects.order_by('user__first_name')
            User = get_user_model()
            users = User.objects.all().values('first_name');
            context = {
                'users': users,
                'status': self.m_user
            }
            return render(request, "mainapp/tableGenerator.html", context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_str = request.POST.get('table')
            table_arr = json.loads(table_str)
            table = Table()
            table.user = request.user
            table.name = request.POST.get('title')
            table.description = request.POST.get('description')
            table.width = len(table_arr[0])
            table.height = len(table_arr)
            table.save()

            for i in range(len(table_arr)):
                for j in range(len(table_arr[0])):
                    cell_arr = table_arr[i][j]
                    if len(cell_arr[0]) > 0:  # берем поля только заполненные, пустые пропускаем
                        # print(cell_arr)
                        if cell_arr[1] == 't' or cell_arr[1] == 'i' or cell_arr[1] == 'f':
                            fields = Field()
                            fields.table = table
                            fields.name = cell_arr[0]
                            fields.description = cell_arr[4]
                            fields.f_type = cell_arr[1]
                            fields.required = cell_arr[5]
                            fields.coord_x = j
                            fields.coord_y = i
                            fields.save()
                        if cell_arr[1] == 'm':
                            permision = Permision()
                            permision.table_created_user = request.user
                            permision.table = table
                            User = get_user_model()
                            user = User.objects.get(first_name=cell_arr[0])
                            permision.user = user
                            permision.coord_x = j
                            permision.coord_y = i
                            permision.save()
                        if cell_arr[1] == 's':
                            fieldExcel = FieldExcel()
                            fieldExcel.table = table
                            fieldExcel.value = cell_arr[0]
                            fieldExcel.coord_x = j
                            fieldExcel.coord_y = i
                            fieldExcel.colspan = cell_arr[2]
                            fieldExcel.save()

            return JsonResponse({'url': '/one-line-table-list'})
        else:
            return redirect('login')

class OneLineTableShow(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            User = get_user_model()
            table_id = request.GET.get('val')
            table_name = Table.objects.filter(id=table_id, user=request.user).values('name', 'id', 'width', 'height')

            permision = Permision.objects.filter(table__id=table_id)
            fields = Field.objects.filter(table__id=table_id)
            fields_data = []# подготовка введеных значений значений
            for use in permision:
                for field in fields:
                    if field.f_type == 't':
                        el = ValueChar.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'i':
                        el = ValueInt.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'f':
                        el = ValueFloat.objects.filter(user=use.user.id, field=field.id).values('value')
                    fields_data.append([el.first(), {'coord_x':field.coord_x, 'coord_y':use.coord_y}])


            permision_values = Permision.objects.filter(table__id=table_id).values()
            fields_values = Field.objects.filter(table__id=table_id).values()
            fields_excel = FieldExcel.objects.filter(table__id=table_id).values()
            table_arr = []
            for i in range(table_name.first()['height']):
                row = []
                temp_colspan = 0
                for j in range(table_name.first()['width']):
                    # table_arr.append()
                    val = ''
                    colspan = 1
                    for el in list(permision_values):#подразделения
                        if(el['coord_x']==j and el['coord_y']==i):
                            val = User.objects.filter(id=el['user_id']).values('first_name').first()['first_name']
                    for el in list(fields_values):#столбики
                        if(el['coord_x']==j and el['coord_y']==i):
                            val = el['name']
                    for el in list(fields_excel):#простой текст и надписи
                        if(el['coord_x']==j and el['coord_y']==i):
                            colspan = el['colspan']
                            val = el['value']
                    for el in fields_data:#значения заплненные пользователями
                        if(el[1]['coord_x']==j and el[1]['coord_y']==i):
                            if el[0] == None:
                                val = ''
                            else:
                                val = el[0]['value']

                    # для пропуска ячеек от colspan
                    if temp_colspan>0:
                        colspan=0
                        temp_colspan=temp_colspan-1
                    if colspan>1:
                        temp_colspan=colspan-1


                    row.append([val, colspan])
                table_arr.append(row)
            # print(table_arr)
            context = {
                'table': table_arr,
                'table_name': table_name,
                'status': self.m_user
            }
            return render(request, "mainapp/tableShow.html", context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.POST.get('val')

            User = get_user_model()

            table_name = Table.objects.filter(id=table_id, user=request.user).values('name', 'id', 'width', 'height')

            permision = Permision.objects.filter(table__id=table_id)
            fields = Field.objects.filter(table__id=table_id)
            fields_data = []  # подготовка введеных значений значений
            for use in permision:
                for field in fields:
                    if field.f_type == 't':
                        el = ValueChar.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'i':
                        el = ValueInt.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'f':
                        el = ValueFloat.objects.filter(user=use.user.id, field=field.id).values('value')
                    fields_data.append([el.first(), {'coord_x': field.coord_x, 'coord_y': use.coord_y, 'f_type': field.f_type}])

            permision_values = Permision.objects.filter(table__id=table_id).values()
            fields_values = Field.objects.filter(table__id=table_id).values()
            fields_excel = FieldExcel.objects.filter(table__id=table_id).values()
            table_arr = []
            for i in range(table_name.first()['height']):
                row = []
                temp_colspan = 0
                for j in range(table_name.first()['width']):
                    # table_arr.append()
                    val = ''
                    m_type = 's'
                    colspan = 1
                    for el in list(permision_values):  # подразделения
                        if (el['coord_x'] == j and el['coord_y'] == i):
                            val = User.objects.filter(id=el['user_id']).values('first_name').first()['first_name']
                            m_type = 'b'
                    for el in list(fields_values):  # столбики
                        if (el['coord_x'] == j and el['coord_y'] == i):
                            val = el['name']
                            m_type = 'b'
                    for el in list(fields_excel):  # простой текст и надписи
                        if (el['coord_x'] == j and el['coord_y'] == i):
                            colspan = el['colspan']
                            val = el['value']
                    for el in fields_data:  # значения заплненные пользователями
                        if (el[1]['coord_x'] == j and el[1]['coord_y'] == i):
                            m_type = el[1]['f_type']
                            if el[0] == None:
                                val = ''
                            else:
                                val = el[0]['value']

                    # для пропуска ячеек от colspan
                    if temp_colspan > 0:
                        colspan = 0
                        temp_colspan = temp_colspan - 1
                    if colspan > 1:
                        temp_colspan = colspan - 1

                    row.append([val, m_type, colspan])
                table_arr.append(row)
            # print(table_arr)

            output = io.BytesIO()
            # Create an new Excel file and add a worksheet.
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()

            # worksheet.set_column(0, 1, 100)  # Увеличиваем ширину
            # worksheet.write(0, 0, 'Муассасалар')  # устанавливаем значение
            # Add a bold format to use to highlight cells.

            #установить ширину колонок по длине текста:
            columns_max_width=[]
            print(table_arr)
            for i in range(len(table_arr[0])):
                max_len = 0
                for j in range(len(table_arr)):
                    cell_value_len = len(table_arr[j][i][0])
                    cell_colspan = table_arr[j][i][2]
                    if cell_value_len>max_len and cell_colspan==1:
                        max_len = cell_value_len
                columns_max_width.append(max_len)
            for index, el in enumerate(columns_max_width):
                worksheet.set_column(index, index, el)


            cell_format_bold = workbook.add_format()
            cell_format_bold.set_bold(True)
            cell_format_bold.set_align('center')
            cell_format_bold.set_align('vcenter')
            # cell_format_bold.set_text_wrap()

            cell_format = workbook.add_format()
            cell_format.set_bold(False)
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            # cell_format.set_text_wrap()

            cell_format_float = workbook.add_format()
            cell_format_float.set_bold(False)
            cell_format_float.set_align('center')
            cell_format_float.set_align('vcenter')
            # cell_format_float.set_text_wrap()
            # cell_format_float.set_num_format('### ### ### ### ##0.00')

            cell_format_int = workbook.add_format()
            cell_format_int.set_bold(False)
            cell_format_int.set_align('center')
            cell_format_int.set_align('vcenter')
            # cell_format_int.set_text_wrap()
            # cell_format_int.set_num_format('### ### ### ### ###')
            print(table_arr)
            for i in range(len(table_arr)):
                for j in range(len(table_arr[0])):
                    cell_value = table_arr[i][j][0]
                    cell_type = table_arr[i][j][1]
                    cell_colspan = table_arr[i][j][2]
                    if cell_colspan > 1:
                        worksheet.merge_range(i, j, i, j+cell_colspan-1, cell_value, cell_format)
                    elif cell_colspan == 0:
                        pass
                    else:
                        if cell_type == 'b':
                            worksheet.write(i, j, cell_value, cell_format_bold)  # устанавливаем значение для жирных (столбик и muassasa)
                        elif cell_type == 'f':
                            worksheet.write(i, j, cell_value, cell_format_float)  # устанавливаем значение для float
                        elif cell_type == 'i':
                            worksheet.write(i, j, cell_value, cell_format_int) # устанавливаем значение для int
                        else:
                            if str(cell_value) != '':
                                if str(cell_value)[0] == '=':
                                    worksheet.write_formula(i, j, cell_value, cell_format)# устанавливаем значение для формулы
                                else:
                                    worksheet.write(i, j, cell_value, cell_format)  # устанавливаем значение

            workbook.close()
            output.seek(0)

            # Set up the Http response.
            filename = slugify(table_name[0]["name"]) + '.xlsx'

            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=' + filename

            return response

            # return redirect('home')
        else:
            return redirect('login')


# не используется
class OneLineTableCopy(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.GET.get('val')


            old_table = list(Table.objects.filter(id=table_id, user=request.user).values())[0]
            # print(old_table)
            new_table = Table()
            new_table.user = request.user
            new_table.name = old_table['name']
            new_table.description = old_table['description']
            new_table.width = old_table['width']
            new_table.height = old_table['height']
            new_table.save()

            old_fields = list(Field.objects.filter(table__id=table_id).values())
            for i in old_fields:
                fields = Field()
                fields.table = new_table
                fields.name = i['name']
                fields.description = i['description']
                fields.f_type = i['f_type']
                fields.required = i['required']
                fields.coord_x = i['coord_x']
                fields.coord_y = i['coord_y']
                fields.save()
            old_permision = list(Permision.objects.filter(table__id=table_id, table_created_user=request.user).values())
            for i in old_permision:
                permision = Permision()
                permision.table_created_user = request.user
                permision.table = new_table
                User = get_user_model()
                user = User.objects.get(id=i['user_id'])
                permision.user = user
                permision.coord_x = i['coord_x']
                permision.coord_y = i['coord_y']
                permision.save()

            old_fieldExcel = list(FieldExcel.objects.filter(table=table_id).values())
            for i in old_fieldExcel:
                fieldExcel = FieldExcel()
                fieldExcel.table = new_table
                fieldExcel.value = i['value']
                fieldExcel.coord_x = i['coord_x']
                fieldExcel.coord_y = i['coord_y']
                fieldExcel.colspan = i['colspan']
                fieldExcel.save()

            return redirect('one-line-table-list')
        else:
            return redirect('login')


class OneLineTableEdit(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.GET.get('val')

            permision = Permision.objects.order_by('user__first_name')
            User = get_user_model()
            users = User.objects.all().values('first_name');
            context = {
                'users': users,
                'status': self.m_user,
                'table_id': table_id
            }
            return render(request, "mainapp/tableGenerator.html", context)
        else:
            return redirect('login')
    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.POST.get('val')

            User = get_user_model()
            # row.push(['', 's', 1, '', '', true]); // value, type, colspan, temp, описание, required
            table_arr = []

            table_name = list(Table.objects.filter(id=table_id, user=request.user).values())[0]
            # print(table_name)

            for i in range(table_name['height']):
                row = []
                for j in range(table_name['width']):
                    row.append(['', 's', 1, '', '', True]); # value, type, colspan, temp, описание, required
                table_arr.append(row)


            permision = list(Permision.objects.filter(table__id=table_id, table_created_user=request.user).values())
            for i in permision:
                cell = []
                User = get_user_model()
                user = User.objects.filter(id=i['user_id']).values('first_name').first()
                cell.append(user['first_name'])# value
                cell.append('m')# type
                cell.append(1)# colspan
                cell.append('')# temp
                cell.append('')# описание
                cell.append(True)# required
                table_arr[i['coord_y']][i['coord_x']] = cell

            fields = list(Field.objects.filter(table__id=table_id).values())
            for i in fields:
                cell = []
                cell.append(i['name'])# value
                cell.append(i['f_type'])# type
                cell.append(1)# colspan
                cell.append('')# temp
                cell.append(i['description'])# описание
                cell.append(i['required'])# required
                table_arr[i['coord_y']][i['coord_x']] = cell
            field_excel = list(FieldExcel.objects.filter(table__id=table_id).values())
            for i in field_excel:
                cell_colspan = i['colspan']
                cell_x = i['coord_x']
                cell_y = i['coord_y']
                cell = []
                cell.append(i['value'])# value
                cell.append('s')# type
                cell.append(cell_colspan)# colspan
                cell.append('')# temp
                cell.append('')# описание
                cell.append(True)# required
                table_arr[cell_y][cell_x] = cell
                if (cell_x + cell_colspan <= table_name['width']):
                    for c in range(1, cell_colspan):
                        x_c = cell_x + c
                        table_arr[cell_y][x_c][1] = 'c'
                        table_arr[cell_y][x_c][0] = ''


            context = {
                'table_data': table_arr,
                'table_name': table_name['name'],
                'table_description': table_name['description']
            }
            return JsonResponse(context)
        else:
            return redirect('login')

class OneLineTableToggleVisable(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.GET.get('val')
            checked = request.GET.get('checked')
            if checked == 'true':
                checked = True
            else:
                checked = False
            Table.objects.filter(id=table_id).update(visable=checked)

            return JsonResponse({'done':'done'})
        else:
            return redirect('login')

#старая не используемая view
def form_constructor(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, "mainapp/formConstructor.html")
    else:
        return redirect('login')

#старая не используемая view
def create_form(request):
    if request.user.is_authenticated and request.user.is_staff:
        table = Table()
        table.name = request.POST.get('table_name')
        table.description = request.POST.get('table_description')
        table.save()

        values = json.loads(request.POST.get('rows'))
        for i in values:
            fields = Field()
            fields.table = table
            fields.name = i['field_name']
            fields.description = i['field_description']
            fields.f_type = i['f_type']
            fields.required = i['required']
            fields.save()
        # print(request.POST)

        return JsonResponse({'url': '/'})
    else:
        return redirect('login')

class configure_table(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.GET.get('val')
            User = get_user_model()
            permision_list = Permision.objects.filter(table_id=table_id).values('user_id')

            left_users = User.objects.all().exclude(id__in=permision_list).values('id', 'first_name')
            right_users = User.objects.filter(id__in=permision_list).values('id', 'first_name')

            return render(request, "mainapp/configureTable.html",
                          {'left': left_users, 'right': right_users, 'table_id': table_id, 'status':self.m_user})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.POST.get('table_id')
            permision_list = Permision.objects.filter(table_id=table_id).values('user_id')
            bd_permision_list_n = [i['user_id'] for i in permision_list]
            if 'data_right[]' in dict(request.POST):
                updated_permision_list = dict(request.POST)['data_right[]']
                updated_permision_list_n = [int(i) for i in updated_permision_list]
            else:
                updated_permision_list_n = []

            # добавляем новые элементы
            for i in updated_permision_list_n:
                if not (i in bd_permision_list_n):
                    # добавить разрешение этому пользователю c id i
                    permision = Permision()
                    permision.table = Table.objects.filter(id=table_id)[0]
                    User = get_user_model()
                    permision.user = User.objects.filter(id=i)[0]
                    permision.save()

            # удаляем отсутствующие элементы
            for i in bd_permision_list_n:
                if not (i in updated_permision_list_n):
                    Permision.objects.filter(user__id=i, table__id=table_id).delete()

            return redirect('home')
        else:
            return redirect('login')

class open_table(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.GET.get('val')
            table_name = Table.objects.filter(id=table_id).values('name', 'id')
            permision = Permision.objects.filter(table__id=table_id).order_by('user__first_name')
            fields = Field.objects.filter(table__id=table_id)
            # print(table_id)
            # table = Table.objects.order_by('-created')
            table_data = []
            for use in permision:
                row = []
                row.append({'user': use})
                for field in fields:
                    if field.f_type == 't':
                        el = ValueChar.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'i':
                        el = ValueInt.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'f':
                        el = ValueFloat.objects.filter(user=use.user.id, field=field.id).values('value')
                    row.append(el)
                table_data.append(row)
            context = {
                'users': permision,
                'fields': fields,
                'table_data': table_data,
                'table_name': table_name,
                'status':self.m_user
            }
            return render(request, "mainapp/openTable.html", context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.POST.get('val')

            table_name = Table.objects.filter(id=table_id).values('name', 'id')
            permision = Permision.objects.filter(table__id=table_id).order_by('user__first_name')
            fields = Field.objects.filter(table__id=table_id)
            fields_values = list(fields.values())
            table_data = []
            for use in permision:
                row = []
                row.append(str(use))

                for field in fields:
                    if field.f_type == 't':
                        el = ValueChar.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'i':
                        el = ValueInt.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'f':
                        el = ValueFloat.objects.filter(user=use.user.id, field=field.id).values('value')
                    if len(el) > 0:
                        row.append(list(el)[0]['value'])
                    else:
                        row.append('')
                table_data.append(row)

            output = io.BytesIO()
            # Create an new Excel file and add a worksheet.
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()

            worksheet.set_column(0, 1, 100)  # Увеличиваем ширину
            # worksheet.write(0, 0, 'Муассасалар')  # устанавливаем значение
            # Add a bold format to use to highlight cells.
            cell_format = workbook.add_format()
            cell_format.set_bold(True)
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            # cell_format.set_text_wrap()

            # заполнение названий колонок
            for i in range(len(fields_values)):
                cell = fields_values[i]['name']

                worksheet.set_column(1 + i, 1 + i, 20)  # устанавливаем ширину
                worksheet.write(0, 1 + i, cell, cell_format)  # устанавливаем значение

            for i in range(len(table_data)):
                cell_format = workbook.add_format()
                cell_format.set_align('center')
                cell_format.set_align('vcenter')
                cell_format.set_bold(True)
                # cell_format.set_text_wrap()
                for j in range(len(table_data[i])):
                    cell = table_data[i][j]

                    # if type(cell)=='str':
                    worksheet.set_column(1 + i, j, 20)  # устанавливаем ширину
                    worksheet.write(1 + i, j, cell, cell_format)  # устанавливаем значение

                    cell_format = workbook.add_format()
                    cell_format.set_align('center')
                    cell_format.set_align('vcenter')
                    cell_format.set_bold(False)
                    # cell_format.set_text_wrap()

            workbook.close()
            output.seek(0)

            # Set up the Http response.
            filename = slugify(table_name[0]["name"]) + '.xlsx'

            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=' + filename

            return response

            # return redirect('home')
        else:
            return redirect('login')


class delite_table(UserStatus, View):
    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            id = request.POST.get("val")
            Table.objects.filter(id=id, user=request.user).delete()
            # table = Table.objects.order_by('-created')
            return redirect('one-line-table-list')
        else:
            return redirect('login')


class client_home(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 't' or self.m_user == 'c' or self.m_user == 'u':#user creator(tanos) or creator or user
            permision = list(Permision.objects.filter(user=request.user).order_by('finished').values())
            permision_data = []
            for i in permision:

                table_name = Table.objects.filter(id=i['table_id']).values('name')

                User = get_user_model()
                creator = User.objects.filter(id=i['table_created_user_id']).values('first_name').first()['first_name']
                if i['finished'] != None:
                    color = 'bg-success'
                    status = '+'
                else:
                    color = 'bg-danger'
                    status = '-'
                permision_el = {
                    'id': i['id'],
                    'name': table_name[0]['name'],
                    'creator': creator,
                    'status': status,
                    'status_color': color,
                    'created': i['created'].strftime("%d.%m.%Y \n %H:%M")
                }
                permision_data.append(permision_el)
            return render(request, "mainapp/clientBase.html", {'table': permision_data, 'navbar':'client-home', 'status':self.m_user, 'user_name': self.user_name})
        else:
            return redirect('login')

class client_fill(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 't' or self.m_user == 'c' or self.m_user == 'u':#user creator(tanos) or creator or user
            permision_id = kwargs['permision_id']
            permission = Permision.objects.filter(id=permision_id).values()
            table_id = list(permission)[0]['table_id']

            table = list(Table.objects.filter(id=table_id).values())

            fields = list(Field.objects.filter(table__id=table_id).values())

            context = {
                'table_id': table_id,
                'permision_id': permision_id,
                'table_name': table[0]['name'],
                'table_description': table[0]['description'],
                'fields': fields,
                'status': self.m_user
            }
            return render(request, "mainapp/clientFill.html", context=context)
        else:
            return redirect('login')


class client_send(UserStatus, View):
    def post(self, request):
        if self.m_user == 't' or self.m_user == 'c' or self.m_user == 'u':#user creator(tanos) or creator or user
            permision_id = request.POST.get('permision_id')
            table_id = request.POST.get('table_id')

            fields = list(Field.objects.filter(table__id=table_id).values())
            for i in fields:
                field_id = i['id']
                field_value = request.POST.get('id' + str(field_id))
                field = Field.objects.get(id=field_id)
                if i['f_type'] == 't':
                    v_char = ValueChar(
                        user=request.user,
                        field=field,
                        value=field_value
                    )
                    v_char.save()
                elif i['f_type'] == 'i':
                    v_int = ValueInt(
                        user=request.user,
                        field=field,
                        value=field_value
                    )
                    v_int.save()
                elif i['f_type'] == 'f':
                    v_float = ValueFloat(
                        user=request.user,
                        field=field,
                        value=field_value
                    )
                    v_float.save()

            permission = Permision.objects.get(id=permision_id)
            permission.finished = datetime.now(timezone.utc)
            permission.save()

            return redirect('client-home')
        else:
            return redirect('login')


class test(View):
    def get(self, request):
        return render(request, "mainapp/test.html")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mainapp/login.html'

    def get_success_url(self):
        User = get_user_model()
        user_data = User.objects.filter(id=self.request.user.id).values('role').first()
        m_user = user_data['role']
        if m_user == 'c' or m_user == 't':#creator or user creator
            return reverse_lazy('home')
        elif m_user == 'u':#user
            return reverse_lazy('client-home')


def logout_user(request):
    logout(request)
    return redirect('login')
