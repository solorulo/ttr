var OBS_MAX_ROWS = 10;
function add_row() {
    if ($('.row').length >= OBS_MAX_ROWS) {
        return;
    }
    var $tbody = $('#tbody');
    var $new_row = $("<tr class=\"row\" meta:new=\"true\"></tr>");

    var $td = $('<td></td>');
    var $button = $("<button class=\"delete_row submit\">-</button>");
    $button.click(function(event) {
        event.preventDefault();
        delete_row($(this));
    });
    $td.append($button);
    // $td.append("<input type=\"text\"/ placeholder=\"Categoría\">");

    $new_row.append($td);
    $new_row.append(
        "<td>"+
        "<textarea class=\"text\" placeholder=\"Descripción ...\" ></textarea>"+
        "</td>");

    $new_select = $("<select></select>");
    for (var key = 0; key < ind_choices.length; key++) {
        var ind_choice = ind_choices[key];
        $new_select.append(
            "<option value="+key+">"+ind_choice+"</option>"
        );
    };
    $new_td = $("<td></td>");
    $new_td.append($new_select);
    $new_row.append($new_td);
    $tbody.append($new_row);
}
function delete_row($obj) {
    var parentRow = $obj.parent().parent();
    parentRow.remove();
}
function send_listaobs() {
    var listaobs = [];
    $('.row').each(function(indexRow, val){
        var $thisRow = $(this);
        var text = $thisRow.find('.text').val();
        var value = $thisRow.find('select').val();
        var meta_index = $thisRow.attr('meta:index');
        listaobs[indexRow] = {
            'text' : text,
            'value' : value,
            'index' : meta_index
        };
    });
    var obj = {
        'titulo' : $('#titulo').val(),
        'autor' : $('#autor').val(),
        'asignatura' : $('#asignatura').val(),
        'oficial' : $('#oficial').is(':checked'),
        'listaobs[]' : JSON.stringify(listaobs),
        "csrfmiddlewaretoken": $.cookie("csrftoken")
    };
    $.post('/instrumento/listaobs/agregar', obj, function(data){
        if (data == "true")
            window.location.href = "/index";
    });
}
$(document).ready(function() {
    $('#add_row').click(function(event) {
        event.preventDefault();
        add_row();
    });
    $(".delete_row").click(function() {
        event.preventDefault();
        delete_row($(this));
    });
    $('#save').click(function(event) {
        send_listaobs();
    });
    // $('button').button();
});
