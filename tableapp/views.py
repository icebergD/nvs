from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
import json

import io
from slugify import slugify
import xlsxwriter

from users.mixins import UserStatus
from .models import Table1, Field1, FieldExcel1, Permision1, ValueChar1, ValueInt1, ValueFloat1

class OneTableList(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table = list(Table1.objects.filter(user=request.user).order_by('-created').values())
            table_data = []

            for i in table:
                permision = Permision1.objects.filter(table__id=i['id'])
                permision_count = len(permision)
                permision_selected = Permision1.objects.filter(table__id=i['id'], finished=None)
                permision_selected_count = len(permision_selected)
                if permision_selected_count == 0 and permision_count != 0:
                    color = 'bg-success'
                elif permision_count == 0:
                    color = 'bg-danger'
                else:
                    color = 'bg-danger'
                table_el = {
                    'id': i['id'],
                    'name': i['name'],
                    'description': i['description'],
                    'status': f'{permision_count - permision_selected_count}/{permision_count}',
                    'status_color': color,
                    'created': i['created']
                }
                table_data.append(table_el)
            # print(table_data)
            return render(request, "tableapp/tablesList.html", {'table': table_data, 'navbar':'one-table-list', 'status':self.m_user})
        else:
            return redirect('login')


class OneTableGenerator(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            permision = Permision1.objects.order_by('user__first_name')
            User = get_user_model()
            users = User.objects.all().values('first_name');
            context = {
                'users': users,
                'status': self.m_user
            }
            return render(request, "tableapp/tableGenerator.html", context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator

            table_arr = json.loads(request.POST.get('table'))
            # print(table_arr)

            table = Table1()
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
                            fields = Field1()
                            fields.table = table
                            fields.name = cell_arr[0]
                            fields.description = cell_arr[4]
                            fields.f_type = cell_arr[1]
                            fields.required = cell_arr[5]
                            fields.coord_x = j
                            fields.coord_y = i
                            fields.save()
                        if cell_arr[1] == 'm':
                            permision = Permision1()
                            permision.table_created_user = request.user
                            permision.table = table
                            User = get_user_model()
                            user = User.objects.get(first_name=cell_arr[0])
                            permision.user = user
                            permision.coord_x = j
                            permision.coord_y = i
                            permision.save()
                        if cell_arr[1] == 's':
                            fieldExcel = FieldExcel1()
                            fieldExcel.table = table
                            fieldExcel.value = cell_arr[0]
                            fieldExcel.coord_x = j
                            fieldExcel.coord_y = i
                            fieldExcel.colspan = cell_arr[2]
                            fieldExcel.save()

            return JsonResponse({'url': '/table/one-table-list'})
        else:
            return redirect('login')


class OneTableShow(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            User = get_user_model()
            table_id = request.GET.get('val')
            table_name = Table1.objects.filter(id=table_id, user=request.user).values('name', 'id', 'width', 'height')

            permision = Permision1.objects.filter(table__id=table_id)
            fields = Field1.objects.filter(table__id=table_id)
            fields_data = []# подготовка введеных значений значений
            for use in permision:
                for field in fields:
                    if field.f_type == 't':
                        el = ValueChar1.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'i':
                        el = ValueInt1.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'f':
                        el = ValueFloat1.objects.filter(user=use.user.id, field=field.id).values('value')
                    fields_data.append([el.first(), {'coord_x':field.coord_x, 'coord_y':use.coord_y}])


            permision_values = Permision1.objects.filter(table__id=table_id).values()
            fields_values = Field1.objects.filter(table__id=table_id).values()
            fields_excel = FieldExcel1.objects.filter(table__id=table_id).values()
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
            return render(request, "tableapp/tableShow.html", context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.POST.get('val')

            User = get_user_model()

            table_name = Table1.objects.filter(id=table_id, user=request.user).values('name', 'id', 'width', 'height')

            permision = Permision1.objects.filter(table__id=table_id)
            fields = Field1.objects.filter(table__id=table_id)
            fields_data = []  # подготовка введеных значений значений
            for use in permision:
                for field in fields:
                    if field.f_type == 't':
                        el = ValueChar1.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'i':
                        el = ValueInt1.objects.filter(user=use.user.id, field=field.id).values('value')
                    elif field.f_type == 'f':
                        el = ValueFloat1.objects.filter(user=use.user.id, field=field.id).values('value')
                    fields_data.append([el.first(), {'coord_x': field.coord_x, 'coord_y': use.coord_y, 'f_type': field.f_type}])

            permision_values = Permision1.objects.filter(table__id=table_id).values()
            fields_values = Field1.objects.filter(table__id=table_id).values()
            fields_excel = FieldExcel1.objects.filter(table__id=table_id).values()
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

            cell_format_bold = workbook.add_format()
            cell_format_bold.set_bold(True)
            cell_format_bold.set_align('center')
            cell_format_bold.set_align('vcenter')
            cell_format_bold.set_text_wrap()

            cell_format = workbook.add_format()
            cell_format.set_bold(False)
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            cell_format.set_text_wrap()

            cell_format_float = workbook.add_format()
            cell_format_float.set_bold(False)
            cell_format_float.set_align('center')
            cell_format_float.set_align('vcenter')
            cell_format_float.set_text_wrap()
            cell_format_float.set_num_format('### ### ### ### ##0.00')

            cell_format_int = workbook.add_format()
            cell_format_int.set_bold(False)
            cell_format_int.set_align('center')
            cell_format_int.set_align('vcenter')
            cell_format_int.set_text_wrap()
            cell_format_int.set_num_format('### ### ### ### ###')

            for i in range(len(table_arr)):
                for j in range(len(table_arr[0])):
                    cell_value = table_arr[i][j][0]
                    cell_type = table_arr[i][j][1]
                    cell_colspan = table_arr[i][j][2]
                    if cell_colspan > 1:
                        worksheet.merge_range(i, j, i, j+cell_colspan, cell_value, cell_format)
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




class OneTableEdit(UserStatus, View):
    def get(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.GET.get('val')

            permision = Permision1.objects.order_by('user__first_name')
            User = get_user_model()
            users = User.objects.all().values('first_name');
            context = {
                'users': users,
                'status': self.m_user,
                'table_id': table_id
            }
            return render(request, "tableapp/tableGenerator.html", context)
        else:
            return redirect('login')
    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            table_id = request.POST.get('val')

            User = get_user_model()
            # row.push(['', 's', 1, '', '', true]); // value, type, colspan, temp, описание, required
            table_arr = []

            table_name = list(Table1.objects.filter(id=table_id, user=request.user).values())[0]
            # print(table_name)

            for i in range(table_name['height']):
                row = []
                for j in range(table_name['width']):
                    row.append(['', 's', 1, '', '', True]); # value, type, colspan, temp, описание, required
                table_arr.append(row)


            permision = list(Permision1.objects.filter(table__id=table_id, table_created_user=request.user).values())
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

            fields = list(Field1.objects.filter(table__id=table_id).values())
            for i in fields:
                cell = []
                cell.append(i['name'])# value
                cell.append(i['f_type'])# type
                cell.append(1)# colspan
                cell.append('')# temp
                cell.append(i['description'])# описание
                cell.append(i['required'])# required
                table_arr[i['coord_y']][i['coord_x']] = cell
            field_excel = list(FieldExcel1.objects.filter(table__id=table_id).values())
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


class OneTableDelite(UserStatus, View):
    def post(self, request, *args, **kwargs):
        if self.m_user == 'c' or self.m_user == 't':#creator or user creator
            id = request.POST.get("val")
            Table1.objects.filter(id=id, user=request.user).delete()
            # table = Table1.objects.order_by('-created')
            return redirect('one-table-list')
        else:
            return redirect('login')
