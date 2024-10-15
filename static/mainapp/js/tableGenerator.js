$( document ).ready(function() {

    var table_created = false;

    const BASE_COUNT = 26;
  function getDivided(num) {
    if (num < 1) {
      return [-1, -1];
    }

    return [Math.floor(num / BASE_COUNT), num % BASE_COUNT]
  }

  function getAlphaFromNum(num) {
    return String.fromCharCode('A'.charCodeAt() + num - 1);
  }

  function calcResult(num) {
    const result = [];

    let divided;

    do {
      const dividedNum = divided ? divided[0] : num;

      divided = getDivided(dividedNum);

      if (divided[1] === 0) {
        divided = [divided[0] - 1, BASE_COUNT]
      }

      if (divided[0] !== -1) {
        result.unshift(getAlphaFromNum(divided[1]));
      }
    } while (divided[0] / BASE_COUNT > 0)

    return result.join('');
  }

   function num2char(num){
        return calcResult(isNaN(num) ? 0 : num) || '*';
   }



    var table = [];



    function tableGenerate(i_columnCnt, i_rowCnt){

        for(var i=0; i<i_rowCnt;i++){
            row =[]
            for(var j=0; j<i_columnCnt;j++){
                row.push(['','s',1,'','',true]);//value,type,colspan, temp, описание, required
            }
            table.push(row)
        }

        drawTable();

    }

    function drawTable(){
        blockCells();

        i_rowCnt = table.length;
        i_columnCnt = table[0].length;
        var thead = '';
        thead +='<tr>';
        for(var j=0; j<i_columnCnt+1;j++){
            thead +='<th scope="col">'+num2char(j)+'</th>';
        }
        thead +='</tr>';
        $("#table-generator-head").html(thead);


        var tbody = ''
        var input_block = $(".table-field").html()

        for(var i=0; i<i_rowCnt;i++){

            tbody+='<tr>';
            tbody+='<th class="table-num-col" scope="row">'+(i+1)+'</th>'
            for(var j=0; j<i_columnCnt;j++){

                if(table[i][j][1]!="c"){
                    tbody+='<td id="'+(i+1)+num2char(j+1)+'" colspan="'+table[i][j][2]+'" data-i="'+i+'" data-j="'+j+'">';

                    //input =   '<input type="text" data-type="t" data-int="'+(i+1)+'" data-char="'+j+'" value="">';
                    //input_block.find( ".btn-group" ).prepend(input);
                    tbody+= input_block;

                    tbody+='</td>';
                }
            }
            tbody+='</tr>';
            $("#table-generator-body").html(tbody);
        }
        confugureTable();
        addNewColRowButtons();
    }
    function confugureTable(){
        i_rowCnt = table.length;
        i_columnCnt = table[0].length;

        for(var i=0; i<i_rowCnt;i++){
            for(var j=0; j<i_columnCnt;j++){
                cell_value = table[i][j][0];
                cell_type = table[i][j][1];
                cell_temp = table[i][j][3];
                cell_descriprion = table[i][j][4];
                if(cell_type!="c"){
                    let input = $("#"+(i+1)+num2char(j+1)+" .fiels-input");
                    let button = $("#"+(i+1)+num2char(j+1)+" button");
                    let description_textarea = $("#"+(i+1)+num2char(j+1)+" .field-description");
                    let colspan = $("#"+(i+1)+num2char(j+1)+" .colspan-btn");
                    if (cell_type == 'm'){
                        input.attr("list","datalistOptions");
                    }
                    else{
                        input.attr("type","text");
                    }

                    if (cell_type == 'm'){
                        input.attr("placeholder","Муассасани қидириш...");
                        $("#"+(i+1)+num2char(j+1)+" .institution-btn").addClass("selected-dropdown");
                    }
                    else if (cell_type == 's'){
                        //input.attr("placeholder","Оддий матн..");
                        $("#"+(i+1)+num2char(j+1)+" .usual-text-btn").addClass("selected-dropdown");
                    }
                    else if (cell_type == 't'){
                        input.attr("placeholder","(Матн тури)Майдон номи...");
                        $("#"+(i+1)+num2char(j+1)+" .text-btn").addClass("selected-dropdown");
                    }
                    else if (cell_type == 'i'){
                        input.attr("placeholder","(Рақам тури)Майдон номи...");
                        $("#"+(i+1)+num2char(j+1)+" .int-btn").addClass("selected-dropdown");
                    }
                    else if (cell_type == 'f'){
                        input.attr("placeholder","(Каср тури)Майдон номи...");
                        $("#"+(i+1)+num2char(j+1)+" .float-btn").addClass("selected-dropdown");
                    }
                    //else{ input.attr("placeholder","Тескт...");}
                    if(cell_temp!='[')//if(cell_temp!='{' && cell_temp!='}' && cell_temp!='[')
                        input.attr("value",cell_value);

                    if(cell_temp=='['){
                        input.attr("disabled","disabled");
                        button.attr("disabled","disabled");
                    }
                    if(cell_type== 't' || cell_type== 'i' || cell_type== 'f')
                        description_textarea.val(cell_descriprion);
                    else{
                        description_textarea.parent().remove();
                    }
                    if(cell_type!='s'){
                        colspan.parent().remove();
                    }
                }
            }
        }
        $(".field-description").change(function() {
            let td = $( this ).parent().parent().parent().parent();
            let i = parseInt(td.attr("data-i"));
            let j = parseInt(td.attr("data-j"));
            let value = String($(this).val());

            table[i][j][4] = value;

        });
        $(".fiels-input").change(function() {
            let td = $( this ).parent().parent();
            let i = parseInt(td.attr("data-i"));
            let j = parseInt(td.attr("data-j"));
            let value = String($(this).val());
            //if(!isNaN(value))
            table[i][j][0] = value;

        });
        //добавить события к кнопкам в выподающем списке
        $(".usual-text-btn").click(function() {
          let td = $( this ).parent().parent().parent().parent();
          let i = td.attr("data-i");
          let j = td.attr("data-j");
          table[i][j][1] = 's';//тип
          table[i][j][0] = '';//значение
          drawTable();
        });
        $(".institution-btn").click(function() {
          let td = $( this ).parent().parent().parent().parent();
          let i = td.attr("data-i");
          let j = td.attr("data-j");
          let cell_value = table[i][j][0];
          let cell_temp = table[i][j][3];
          if(cell_temp!='{' && cell_temp!='}' && cell_temp!='['){
              table[i][j][1] = 'm';//тип
              table[i][j][0] = '';//значение
              drawTable();
          }
          else{
            alert("Операцияни бажариш мумкин емас");
          }

        });
        $(".my-required-btn input").click(function() {
          let td = $( this ).parent().parent().parent().parent().parent();
          let i = td.attr("data-i");
          let j = td.attr("data-j");

          table[i][j][5] = $( this ).is(':checked');
//          let cell_value = table[i][j][0];
//          let cell_temp = table[i][j][3];
//          if(cell_temp!='{' && cell_temp!='}' && cell_temp!='['){
//              table[i][j][1] = 'i';//тип
//              table[i][j][0] = '';//значение
//              drawTable();
//          }
//          else{
//            alert("Операцияни бажариш мумкин емас");
//          }

        });
        $(".int-btn").click(function() {
          let td = $( this ).parent().parent().parent().parent();
          let i = td.attr("data-i");
          let j = td.attr("data-j");
          let cell_value = table[i][j][0];
          let cell_temp = table[i][j][3];
          if(cell_temp!='{' && cell_temp!='}' && cell_temp!='['){
              table[i][j][1] = 'i';//тип
              table[i][j][0] = '';//значение
              drawTable();
          }
          else{
            alert("Операцияни бажариш мумкин емас");
          }

        });
        $(".float-btn").click(function() {
          let td = $( this ).parent().parent().parent().parent();
          let i = td.attr("data-i");
          let j = td.attr("data-j");
          let cell_value = table[i][j][0];
          let cell_temp = table[i][j][3];
          if(cell_temp!='{' && cell_temp!='}' && cell_temp!='['){
              table[i][j][1] = 'f';//тип
              table[i][j][0] = '';//значение
              drawTable();
          }
          else{
            alert("Операцияни бажариш мумкин емас");
          }

        });
        $(".text-btn").click(function() {
          let td = $( this ).parent().parent().parent().parent();
          let i = td.attr("data-i");
          let j = td.attr("data-j");
          let cell_value = table[i][j][0];
          let cell_temp = table[i][j][3];
          if(cell_temp!='{' && cell_temp!='}' && cell_temp!='['){
              table[i][j][1] = 't';//тип
              table[i][j][0] = '';//значение
              drawTable();
          }
          else{
            alert("Операцияни бажариш мумкин емас");
          }
        });
        $(".colspan-btn").click(function() {

            let td = $( this ).parent().parent().parent().parent();
            let i = parseInt(td.attr("data-i"));
            let j = parseInt(td.attr("data-j"));
            let colspan = prompt("нечта майдонни бирлаштириш керак?");
            if(colspan!=null){
                 colspan = parseInt(colspan);
                 if(!isNaN(colspan)){
                    if(j+colspan<=table[0].length){
                        table[i][j][2] = colspan;
                        for(var c=1;c<colspan;c++){
                            let j_c = j+c;
                            table[i][j_c][1] = "c";
                            table[i][j_c][0] = "";
                        }
                        drawTable();
                    }
                    else{
                        alert("Жадвалдан ташқари");
                    }

                 }
                 else{
                    alert("Нотўғри рақам киритилган");
                 }
            }
            else{
                alert("Нотўғри рақам киритилган");
            }
            //let cell_value = table[i][j][0];

        });



    }

    function blockCells(){
        i_rowCnt = table.length;
        i_columnCnt = table[0].length;
        let clumns = [];
        let permisions = [];

        for(var i=0; i<i_rowCnt;i++){
            for(var j=0; j<i_columnCnt;j++){
                cell_value = table[i][j][0];
                cell_type = table[i][j][1];
                cell_temp = table[i][j][3];
                if(cell_temp=="{" || cell_temp=="}" || cell_temp=="["){//отчиска таблицы от этих символов, чтоб потом заново нарисовать
                    table[i][j][3] = "";
                }
                if(cell_type=='m'){
                    permisions.push([i,j]);
                }
                if(cell_type=='i' || cell_type=='f' || cell_type=='t'){
                    clumns.push([j,i]);
                }
            }
        }
        for(var i=0; i<i_rowCnt;i++){
            for(var j=0; j<i_columnCnt;j++){
                clumns.forEach(function(colum){
                  if(j==colum[0] && i!=colum[1]){
                    table[i][j][3] = '{';
                  }
                })
                permisions.forEach(function(perm){
                  if(i==perm[0] && j!=perm[1]){
                    if(table[i][j][3]=='{'){
                        table[i][j][3] = '[';
                    }
                    else{
                        table[i][j][3] = '}';
                    }

                  }
                })
            }
        }
    }

    function addNewColRowButtons(){
        $('#table-generator-head tr').append('<th><button id="addColBtn" class="btn btn-outline-secondary">+</button></th>')
        $('#table-generator-body').append('<tr><td><button id="addRowBtn" class="btn btn-outline-secondary">+</button></td></tr>')
        $('#addColBtn').click(function(){
            let i_rowCnt = table.length;
            let i_columnCnt = table[0].length;
            for(var i=0; i<i_rowCnt;i++){
                table[i].push(['','s',1,'','',true]);//value,type,colspan, temp, описание, required
            }
            drawTable();
        })
        $('#addRowBtn').click(function(){
            let i_rowCnt = table.length;
            let i_columnCnt = table[0].length;

            row =[]
            for(var j=0; j<i_columnCnt;j++){
                row.push(['','s',1,'','',true]);//value,type,colspan, temp, описание, required
            }
            table.push(row)

            drawTable();
        })
    }



    $('#tableCreateModalBtn').click(function(){
        $('td.SizeChooser-hover').removeClass('SizeChooser-hover');
        $('#md-table-gen-chooser td').removeClass('SizeChooser-selected');
        $('#md-table-gen-chooser td').removeClass('SizeChooser-hover');
        $('#md-table-gen-wrap').hide('slow');

    })
    $('#tableCreateBtn').click(function(){
        var col = parseInt($("#colValue1").val());
        var raw = parseInt($("#rawValue1").val());
        if(isNaN(col) || isNaN(raw)){
            alert("Майдонларни бўш қолдириш мумкин емас");
        }
        else{
            if(table_created){
                alert("Жадвал аллақачон яратилган");
            }
            else{
                tableGenerate(col, raw);
                table_created = true;
            }

        }
    })

    var columns;
    var rows;
    var columnCnt;
    var rowCnt;


    $(function() {
      $('#md-table-gen-chooser td').hover(function() {
        var n = $(this).index();
        var m = $(this).parent('tr').index();
        $('#md-table-gen-chooser td').removeClass('SizeChooser-hover');
        $('#md-table-gen-chooser tr').each(function(y) {
          $(this).find('td').each(function(x) {
            if (x <= n && y <= m) {
              $(this).addClass('SizeChooser-hover');
            }
          })
        })
      }).click(function(){

        columns = $(this).index();
        rows = $(this).parent('tr').index();
        columnCnt = columns+1;
        rowCnt = rows+1;
        if(table_created){
            alert("Жадвал аллақачон яратилган");
        }
        else{
            tableGenerate(columnCnt, rowCnt);
            table_created = true;
        }


        $('#md-table-gen-chooser td').removeClass('SizeChooser-selected');
        $('td.SizeChooser-hover').addClass('SizeChooser-selected');


        $('td.SizeChooser-hover').removeClass('SizeChooser-hover');
        $('#md-table-gen-chooser td').removeClass('SizeChooser-selected');
        $('#md-table-gen-chooser td').removeClass('SizeChooser-hover');
        $('#md-table-gen-wrap').hide('slow');

      });
    });

    $('#md_add_table').click(function (e) {
        $("#md-table-gen-wrap").css({
            'position': 'absolute',
                'left': $(this).offset().left,
                'top': $(this).offset().top + $(this).height() + 5
        }).show("slow");
    });



    $("#table-save").click(function (e) {
        console.log("sssssssssss")
        console.log(table)
        console.log("sssssssssss")
        let title = $("#table-title").val();
        let description = $("#table-description").val();
        if(title.length>0 && description.length>0){
            if(table_created==true){
                if(tableContains("m")){
                    if(tableContains("t") || tableContains("i") || tableContains("f")){
                        sendTableToBackend(title, description);
                    }
                    else{
                        alert("Тўлдириш учун устунлар йўқ");
                    }
                }
                else{
                    alert("Жадвални ким тўлдириши аниқланмаган (муассаса)");
                }
            }
            else{
                alert("Жадвал яратилмаган");
            }

        }
        else{
            alert("Жадвал номи ёки тавсифи бўш қолдирилган");
        }

    });
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function my_ajax(t_name, t_description){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/one-line-table-generator',
            method: 'post',
            dataType: 'json',
            data: {'csrfmiddlewaretoken' :  csrftoken, 'title': t_name, 'description':t_description, 'table':JSON.stringify(table)},
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
    function my_ajax_edit_table(l_table_id){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/one-line-table-edit',
            method: 'post',
            dataType: 'json',
            data: {'csrfmiddlewaretoken' :  csrftoken, 'val': l_table_id},
            success: function(data){
                table = data.table_data;
                drawTable();
                $("#table-title").val(data.table_name)
                $("#table-description").val(data.table_description)
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
                table_created=false;
            }
        });
        return "none"
    }
    function sendTableToBackend(title, description){
        my_ajax(title, description);
    }
    var table_id = $("#table_id").val();
    if(table_id.length>0){
        table_created = true;
        my_ajax_edit_table(Number(table_id))
    }
    function usersArray(){
        return $('#datalistOptions').children().toArray().map(el => el.value);
    }
    function tableContains(char){
        i_rowCnt = table.length;
//        console.log("i_rowCnt "+i_rowCnt);
        i_columnCnt = table[0].length;
//        console.log("i_columnCnt "+i_columnCnt);
        let charArr = 0;
        let users_arr = usersArray();

        for(var i=0; i<i_rowCnt;i++){
            for(var j=0; j<i_columnCnt;j++){
//                console.log(i);
//                console.log(j);
//                console.log(table);
//                console.log(table[i][j]);
//                console.log(table[i][j][1]);
//                console.log(char);
                let cell_type = table[i][j][1];
//                console.log(cell_type==char);
                if(cell_type==char){
                    let cell_value = table[i][j][0];
                    if(char=='t'||char=='i'||char=='f'){
                        if(cell_value.length>0){
                            charArr++;
                        }
                    }
                    else if(char=='m'){
                        if(cell_value.length>0){
                            for (var k = 0; k < users_arr.length; k++) {
                                if (users_arr[k] == cell_value) {
                                    charArr++;
                                }
                            }

                        }
                    }

                }

            }
        }
        if(charArr>0){
            return true;
        }
        return false;
    }



});


















