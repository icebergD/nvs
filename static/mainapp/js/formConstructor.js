$( document ).ready(function() {
    var table_rows = $('#table-rows');
    var data_structure = [];

    function my_ajax(t_name, t_description, arr){
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: '/create-form',
            method: 'post',
            dataType: 'json',
            data: {table_name:t_name, table_description:t_description, rows: JSON.stringify(arr), csrfmiddlewaretoken: csrf},
            success: function(data){
                window.location = data.url;
            },
            error: function (jqXHR, exception) {
                if (jqXHR.status === 0) {
                    alert('Not connect. Verify Network.');
                } else if (jqXHR.status == 404) {
                    alert('Requested page not found (404).');
                } else if (jqXHR.status == 500) {
                    alert('Internal Server Error (500).');
                } else if (exception === 'parsererror') {
                    alert('Requested JSON parse failed.');
                } else if (exception === 'timeout') {
                    alert('Time out error.');
                } else if (exception === 'abort') {
                    alert('Ajax request aborted.');
                } else {
                    alert('Uncaught Error. ' + jqXHR.responseText);
                }
            }
        });

    }
    $("#create-btn-id").click(function(e) {
        e.preventDefault();
        var table_name = $("#table_name").val()
        var table_description = $("#table_description").val()
        var arr_empty = 0;
        for(var i=0; i<data_structure.length; i++){
            if(data_structure[i]!=undefined){
                arr_empty++;
            }
        }
        if(table_name!=""){//проверка не осталось ли пустым поле название таблици
            if(arr_empty>0){//проверка добавлены ли дополнительные поля

                //убираем из массива все undefined
                var result = []
                for(var i=0; i<data_structure.length; i++){
                    if(data_structure[i]!=undefined){
                        result.push(data_structure[i]);
                    }
                }
                my_ajax(table_name, table_description, result);//вызов ajax функции, отправляем все нужные данные
            }
            else{
                alert("Майдонлар қўшилмаган");
            }
        }
        else{
            alert("Жадвал номини то\'лдиринг");
        }


    });

    $("#add-box-form").click(function() {

        field_name = $('#field_name').val();
        field_description = $('#field_description').val();

        f_type = $('#f_type option:selected').text();



        if ($('#field_required').is(":checked"))
        {
            field_required = true;
            m_required = '*';
        }
        else{
            field_required = false;
            m_required = ' '
        }

        if(field_name==''){
            alert('Майдон номини то\'лдиринг')
        }
        else{

            var structure_element = {
                'field_name': field_name,
                'field_description': field_description,
                'required': field_required,
                'f_type': $('#f_type').val()
            }
            data_structure.push(structure_element)
            //alert(data_structure[0]["field_name"])


            var bot_html =''
            //bot_html +=                 '<section class="form-box">';
            bot_html +=                     '<div class="row">'
            bot_html +=                         '<h3 class="col-sm">'+field_name+'<span class="must">'+m_required+'</span></h3>'
            bot_html +=                         '<div class="col-sm">'
            bot_html +=                             '<button type="button" class="float-end close close-btn" value="'+data_structure.length+'">'
            bot_html +=                                 '<span aria-hidden="true">&times;</span>'
            bot_html +=                             '</button>'
            bot_html +=                         '</div>'
            bot_html +=                     '</div>'
            bot_html +=                     '<div class="form-group">'
            bot_html +=                         '<div>Майдон тури: <span>'+f_type+'</span></div>'
            bot_html +=                     '</div>'
            bot_html +=                     '<div class="form-group">'
            bot_html +=                         '<label>Тавсифи:</label>'
            bot_html +=                         '<div>'+field_description+'</div>'
            bot_html +=                     '</div>'
            //bot_html +=                 '</section>'

            d = document.createElement('section');
            $(d).addClass('form-box').html(bot_html).appendTo(table_rows);//добавление элемента на html


            //отчистка модального окна
            $('#exampleModal').modal('hide');
            $('#field_name').val('');
            $('#field_description').val('');
            $('#f_type').val('t');
            $('#field_required').prop('checked', true);

            $(".close-btn").click(function() {
                var index = $(this).val()-1;

                $(this).parent().parent().parent().remove()
                delete data_structure[index]
            });

        }

    });




});








