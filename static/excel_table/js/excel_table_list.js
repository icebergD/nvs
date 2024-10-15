$( document ).ready(function() {

    $(".delet-btn").click(function(e) {
        var id = $(this).val();

        $(".delet-btn-final").val(id)

    });
    $(".visable-toggle").change(function(e) {

        var id = $(this).val();
        var checked = $(this).prop('checked');
        toggle_ajax(id, checked);


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
    function toggle_ajax(table_id, checked){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/excel/excel-table-toggle-visable',
            method: 'get',
            dataType: 'json',
            data: {'csrfmiddlewaretoken':  csrftoken, 'val': table_id, 'checked': checked},
            success: function(data){

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

});








