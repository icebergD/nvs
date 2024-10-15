
////усанавливаем нужную высоту таплицы
//const windowInnerWidth = window.innerWidth;
//const windowInnerHeight = window.innerHeight;
//var tableWraper = document.querySelector(".tab-body-wrap");
//tableWraper.style.height = windowInnerWidth*1.0+"px";

let table_body = document.querySelector(".chosen-tab-body");
$(".scrollbar-content").width(table_body.scrollWidth);

$(".scrollbar-table").scroll(function() {
var target = $(".chosen-tab-body");
  target.prop("scrollTop", this.scrollTop)
        .prop("scrollLeft", this.scrollLeft);
});

function openTab(evt, tabNum) {
  tabStateName = tabNum;
  var i, x, tablinks;
  x = document.getElementsByClassName("tab-body");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
    x[i].className = x[i].className.replace(" chosen-tab-body", "");
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < x.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" chosen-tab", "");
  }
  let table_body = document.getElementById(tabNum);
  table_body.style.display = "block";
  evt.currentTarget.className += " chosen-tab";
  table_body.className += " chosen-tab-body";
  $(".scrollbar-content").width(table_body.scrollWidth);
}
/*
function showIt(row, col) {
    const el = document.querySelector('#'+tabStateName+' td[data-row="' + row + '"][data-col="' + col + '"]');
    //var el = document.getElementById(elID);
    el.scrollIntoView(true);
}*/
////showIt(15, 14);



function getInputValues() {
//    const el = document.querySelector('#'+tabStateName+' td[data-row="' + row + '"][data-col="' + col + '"]');
    let cells_input = document.getElementsByClassName('cell_input');
    console.log(cells_input);

    let input_values = [];
    for(let i=0; i<cells_input.length; i++){

        const cell = cells_input[i];
        input_values.push({ row: cell.getAttribute("data-row"), col: cell.getAttribute("data-col"), sheet: cell.parentNode.parentNode.parentNode.parentNode.parentNode.getAttribute("id"), value: cell.value });
    }
    return input_values;
}

function checkEmptyCells(input_values){
    for(let i=0; i<input_values.length; i++){
        if(input_values[i]['value']==''){
            return false;
        }
    }
    return true;
}

$(".save-btn").click(function(event) {
    console.log("save");
    let input_values = getInputValues();
    if(!checkEmptyCells(input_values)){
        var myModal = new bootstrap.Modal(document.getElementById("exampleModal"));
        let modal_body = $("#exampleModal .modal-body");
        let message = 'Барча ҳужайралар тўлдирилмади, бўш қолади';
        modal_body.html(message);
        myModal.show();
    }
    else{
        my_ajax(input_values);
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

function my_ajax(input_values){
    var csrftoken = getCookie('csrftoken');
    var input_values_a = JSON.stringify(input_values);
    var table_id = $("#table_id").val();
    var url = '/excel/client-excel-fill/'+table_id+'/'
    console.log(url);
    $.ajax({
        type: 'post',
        method: 'post',
        dataType: "json",
        data: {input_values: input_values_a, csrfmiddlewaretoken: csrftoken},
        success: function(data){
            console.log(data);
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
