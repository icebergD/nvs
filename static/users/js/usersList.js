$( document ).ready(function() {

    $(".delet-btn").click(function(e) {
        var id = $(this).val();

        $(".delet-btn-final").val(id)

    });


});
