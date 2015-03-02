// var COTEJO_MAX_ROWS = 10;
// var id_inst;
function request_comments() {
    $.ajax({
        url: '/instrumento/comentarios/?id='+id_inst,
        type: 'GET',
        success: load_comments,
        error: function() {
            alert("Error");
        },
        headers: {
            'X-CSRFToken': $.cookie("csrftoken")
        },
    });
}
function load_comments(data) {
    console.log(data);
    $('#comments_section').empty();
    for (var i = 0; i < data.length; i++) {
        var obj = data[i];
        var pk = obj.pk;
        var texto = obj.texto;
        var user = obj.user;
        $('#comments_section').append(
            "<article class='comment'>" +
            "<div><b>" + user.full_name + "</b></div>" +
            "<div>" + texto + "</div>" +
            "</article>"
        );
    };
}
function send_comment() {
    var obj = {
        'id' : id_inst,
        'text' : $('#comment_add textarea').val(),
        //'user_id' : '2',
        "csrfmiddlewaretoken": $.cookie("csrftoken")
    };
    $.post('/instrumento/comentario/', obj, function(data){
        if (data == "true")
            request_comments();
    });
}
$(document).ready(function() {
    $('#comment_add button').click(function(event) {
        event.preventDefault();
        send_comment();
    });
    request_comments();
});
