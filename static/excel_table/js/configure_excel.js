let isSelecting = false;
let startRow, startCol;
let selectedCells = [];
let tabStateName = $("#active_sheet_id").val();

let Users = []
let UsersSelectedCells = []

UsersSelectedCells = window.storage.users_selected_cells;
Users = window.storage.selected_users;
console.log("start value UsersSelectedCells ", UsersSelectedCells)
console.log("start value Users ", Users)
drowDownListSelect();
/*
document.addEventListener('mousedown', (event) => {
  const cell = event.target;
  if (cell.nodeName === 'TD') {
    isSelecting = true;
    startRow = parseInt(cell.getAttribute("data-row"));//parseInt(cell.id.split('-')[0]);
    startCol = parseInt(cell.getAttribute("data-col"));//parseInt(cell.id.split('-')[1]);
    selectCells(startRow, startCol, startRow, startCol, event.ctrlKey);
  }
});*/



document.addEventListener('mousedown', (event) => {
  const cell = event.target;
  if (cell.nodeName === 'TD') {
    const isAlreadySelected = selectedCells.includes(cell);
    isSelecting = true;
    startRow = parseInt(cell.getAttribute("data-row"));
    startCol = parseInt(cell.getAttribute("data-col"));
    selectCells(startRow, startCol, startRow, startCol, event.ctrlKey);
    if (isAlreadySelected) {
      cell.classList.remove('selected');
      const cellIndex = selectedCells.indexOf(cell);
      if (cellIndex > -1) {
        selectedCells.splice(cellIndex, 1);
      }
    }
  }
});

document.addEventListener('mousemove', (event) => {
  if (isSelecting && event.buttons === 1) {
    const cell = event.target;
    if (cell.nodeName === 'TD') {
      const endRow = parseInt(cell.getAttribute("data-row"));//parseInt(cell.id.split('-')[0]);
      const endCol = parseInt(cell.getAttribute("data-col"));//parseInt(cell.id.split('-')[1]);
      selectCells(startRow, startCol, endRow, endCol, event.ctrlKey);
    }
  }
});

document.addEventListener('mouseup', (event) => {
  const cell = event.target;
  if (cell.nodeName === 'TD') {
      isSelecting = false;
      const selectedCellIds = selectedCells;
      setActiveCells(selectedCells);
      console.log(selectedCellIds);
  }
});

function selectCells(startRow, startCol, endRow, endCol, isAdditiveSelection) {
  if (!isAdditiveSelection) {
    // Clear previous selections
    for(let i=0; i<selectedCells.length; i++){
        const cell = selectedCells[i]
        //const cell_obj = document.querySelector('#'+cell["sheet"]+' td[data-row="' + cell["row"] + '"][data-col="' + cell["col"] + '"]');
        cell.classList.remove('selected')
    }

//    selectedCells.forEach(cell => cell.classList.remove('selected'));
    selectedCells = [];
  }

  for (let row = Math.min(startRow, endRow); row <= Math.max(startRow, endRow); row++) {
    for (let col = Math.min(startCol, endCol); col <= Math.max(startCol, endCol); col++) {
      //const cell = document.getElementById(`${row}-${col}`);
      const cell = document.querySelector('#'+tabStateName+' td[data-row="' + row + '"][data-col="' + col + '"]');
      if (!selectedCells.includes(cell)) {
        cell.classList.add('selected');
        selectedCells.push(cell);//{"sheet":tabStateName, "row": row, "col":col});
      }
    }
  }
}

function getSelectedCellIds(cells_arr) {
    return cells_arr;
//  console.log(typeof(cells_arr))
//  const selectedIds = cells_arr.map(cell => ({ row: cell.getAttribute("data-row"), col: cell.getAttribute("data-col"), sheet: cell.parentNode.parentNode.parentNode.parentNode.getAttribute("id") }));
//  return selectedIds;
}

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
//showIt(15, 14);


//-----------------
//dropdown
$(document).on('click', function(event) {
  if (!$(event.target).closest('.dropdown').length) {
   $('.option-list, .search-box').hide();
  }
});
$('.select').click(function(event) {
  //$('.option-list, .search-box').hide();
  $(this).closest('.dropdown').find('.option-list, .search-box').toggle();
  $('.option-list a').click(function(){
    var select = $(this).text();
    $(this).closest('.dropdown').children('.select').text(select);
    $('.option-list, .search-box').hide();

  });
});
$('.option-list').click(function(event){
    let selected_user = $(".select").text();
    console.log(selected_user);
    setActiveUser(selected_user);
});
//Search
$('.seach-control').keyup(function(){
 var val = $(this).val().toLowerCase();
 var list =  $(this).closest('.dropdown').find('li')
  list.each(function()
   {
     var text = $(this).text().toLowerCase();
     if(text.indexOf(val)==-1)
       {
         $(this).hide();
       }
     else
       {
         $(this).show();
       }

   })
});

//dropdown end
//-----------------

//выделить ячейки по массиву
function selectAllCells(ojectsArr){
    if(ojectsArr != ''){
        let ff = ojectsArr;//getSelectedCellIds(ojectsArr)
        deselectAllCells();
        console.log(ff);
        ff.forEach(obj => {
            const rowValue = obj["row"];
            const colValue = obj["col"];
            const cell = document.querySelector('#'+obj.sheet+' td[data-row="' + rowValue + '"][data-col="' + colValue + '"]');
            if (!selectedCells.includes(cell)) {
                cell.classList.add('selected');
                selectedCells.push(cell);
            }
        });
    }
    else{
        deselectAllCells();
    }
}

//отменить выделение
function deselectAllCells(){
    $(".tab-body")
    let selected_cells = document.querySelectorAll('.tab-body td.selected');

    selected_cells.forEach(cell => cell.classList.remove('selected'));
    selectedCells = [];
    console.log("cleared");
}

//при переключении пользователя
function setActiveUser(user){
    if (!Users.includes(user) && user!= "Фойдаланувчини танланг") { //если пользователь новый, добавить в массив и отчистить выделенные ячейки
        //cell.classList.add('selected');
        Users.push(user);
        UsersSelectedCells.push("");
        deselectAllCells();
    }
    else{ //если пользователь уже есть, то выделить ячейки
        user_index = Users.indexOf(user);
        console.log("index: "+user_index);
        if(user_index != -1){
            let cells_obj = UsersSelectedCells[user_index];
            selectAllCells(cells_obj);
        }
    }
    drowDownListSelect();
    console.log("function setActiveUser: ",Users);
    console.log("function setActiveUser: ", UsersSelectedCells);
}
//при каждом выделении ячеек, установить выделенные ячейки конкретному пользователю
function setActiveCells(arr_obj){
    let active_user = $(".select").text();
    user_index = Users.indexOf(active_user);
    if(user_index != -1){
        let temp_cells = [];
        arr_obj.forEach(cell => {
            const rowValue = parseInt(cell.getAttribute("data-row"));
            const colValue = parseInt(cell.getAttribute("data-col"));
            const sheetValue = cell.parentNode.parentNode.parentNode.parentNode.getAttribute("id");
            temp_cells.push({"sheet": sheetValue, "col": colValue, "row": rowValue});
        });
        UsersSelectedCells[user_index] = temp_cells;
    }
}

function checkCrossOverCells(cells_arrays, users){
//    array = []
//    for(let i=0;i<cells_arrays.length;i++){
//        const el = cells_arrays[i];
//        if(el!=''){
//            array.push(getSelectedCellIds(el));
//        }
//    }
    array = cells_arrays;
    console.log('checkCrossOverCells');
    console.log(array)
    output_cells = [];
    for (let i = 0; i < array.length; i++) {
        for (let j = i+1; j < array.length; j++) {
//            console.log(array[i]);
//            console.log(array[j]);

            for (let l = 0; l < array[i].length; l++) {
                for (let k = 0; k < array[j].length; k++) {
                    let el1 = array[i][l];
                    let el2 = array[j][k];
                    console.log(el1);
                    console.log(el2);
                    if(el1['row']==el2['row'] && el1['col']==el2['col'] && el1['sheet']==el2['sheet']){
                        const result = {
                            user1:users[i],
                            user2:users[j],
                            cells:el1
                        }
                        output_cells.push(result);

                    }

                }
            }
            //console.log("__");
        }
    }
    console.log(output_cells);
    return output_cells;
}

function convertNumberToChar(number) {
  let dividend = number;
  let columnName = '';
  let modulo;

  while (dividend > 0) {
    modulo = (dividend - 1) % 26;
    columnName = String.fromCharCode(65 + modulo) + columnName;
    dividend = Math.floor((dividend - modulo) / 26);
  }

  return columnName;
}
//-----------------------------------------------------
$(".save-btn").click(function(event) {
  console.log("save");

  const cross_cells = checkCrossOverCells(UsersSelectedCells, Users)
  if(cross_cells.length != 0){
    var myModal = new bootstrap.Modal(document.getElementById("exampleModal"));
    let modal_body = $("#exampleModal .modal-body");
    let message = ''
    for(let i=0;i<cross_cells.length;i++){
        const cell = cross_cells[i]["cells"];
        //let tab_name = $("button.tablink").find("[data-tab-id='"+cell["sheet"]+"}']").text();
        let tab_name = $(".tablink[data-tab-id='" + cell["sheet"] +"']").text();
        message += "<p><b>"+convertNumberToChar(cell["col"])+cell["row"]+"</b> <span>"+tab_name+"</span> <u>"+cross_cells[i]["user1"]+"</u> ва <u>"+cross_cells[i]["user2"]+ "</u></p>"
    }

    modal_body.html(message);
    myModal.show();

  }
  else{
    my_ajax(Users, UsersSelectedCells)

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
function my_ajax(users_arr_obj, users_cells_arr_obj){
    var csrftoken = getCookie('csrftoken');
    let user_arr = []
    let users_cells_arr = []
    for(let i=0;i<users_cells_arr_obj.length;i++){
        const el = users_cells_arr_obj[i];
        if(el!='' && el.length>0){
            users_cells_arr.push(getSelectedCellIds(el));
            user_arr.push(users_arr_obj[i]);
        }
    }
    console.log(user_arr);
    console.log(users_cells_arr);
    $.ajax({
        method: 'post',
        dataType: 'json',
        data: {users: JSON.stringify(user_arr), users_cells: JSON.stringify(users_cells_arr), csrfmiddlewaretoken: csrftoken},
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

//-------------------------------------------------------
function drowDownListSelect(){
    //Users
//    let users_li = document.querySelector(".option-list li");
//    alert(users_li)
//    for (let i = 0; i <= users_li.length - 1; i++) {
//        alert(users_li[i])
//    }
    let users_li = $(".option-list li");
    let users_li_a = $(".option-list li a");
    for (let i = 0; i <= users_li.length - 1; i++) {
        user_text = users_li_a[i].text;
        console.log(UsersSelectedCells[i]);
        users_li[i].classList.remove('selected-user');
        if (Users.includes(user_text)) {
            let index = Users.indexOf(user_text)
            console.log(UsersSelectedCells[index]);
            if(UsersSelectedCells[index]==""){
                continue;
            }
            else if(UsersSelectedCells[index].length == 0){
                continue;
            }
            users_li[i].classList.add('selected-user');

        }
    }

}
