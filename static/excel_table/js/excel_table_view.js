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


$(".save-btn").click(function(event) {
//    console.log("save");
//    let input_values = getInputValues();
//    if(!checkEmptyCells(input_values)){
//        var myModal = new bootstrap.Modal(document.getElementById("exampleModal"));
//        let modal_body = $("#exampleModal .modal-body");
//        let message = 'Барча ҳужайралар тўлдирилмади, бўш қолади';
//        modal_body.html(message);
//        myModal.show();
//    }
//    else{
//        my_ajax(input_values);
//    }
});
