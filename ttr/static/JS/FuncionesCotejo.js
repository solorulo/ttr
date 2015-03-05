var COTEJO_MAX_ROWS = 10;
function add_row() {
    if ($('.row').length >= COTEJO_MAX_ROWS) {
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
        "<textarea class=\"text\" placeholder=\"Descripción\" ></textarea>"+
        "</td>");
    $new_row.append(
        "<td class='checkbox_center'>"+
        "<input type=\"checkbox\" />"+
        "</td>");
    $new_row.append(
        "<td>"+
        "<textarea class=\"observ\" placeholder=\"Observaciones\" ></textarea>"+
        "</td>");
    // <td>
    //     <input type="text" value="4" />
    // </td>
    // <td>
    //     <input type="checkbox" />
    // </td>
    $tbody.append($new_row);
}
function delete_row($obj) {
    var parentRow = $obj.parent().parent();
    parentRow.remove();
}
function send_listacotejo() {
    var listacotejo = [];
    var pk_inst = $('#pk_inst').val();
    $('.row').each(function(indexRow, val){
        var $thisRow = $(this);
        var text = $thisRow.find('.text').val();
        var observ = $thisRow.find('.observ').val();
        var checked = $thisRow.find('input[type=checkbox]').is(':checked');
        var meta_index = $thisRow.attr('meta:index');
        listacotejo[indexRow] = {
            'text' : text,
            'observ' : observ,
            'checked' : checked,
            'index' : meta_index
        };
    });
    var obj = {
        'titulo' : $('#titulo').val(),
        'autor' : $('#autor').val(),
        'asignatura' : $('#asignatura').val(),
        'oficial' : $('#oficial').is(':checked'),
        'listacotejo[]' : JSON.stringify(listacotejo),
        "csrfmiddlewaretoken": $.cookie("csrftoken")
    };
    var url = (pk_inst) ? 
        '/instrumento/listacotejo/editar?id='+pk_inst : 
        '/instrumento/listacotejo/agregar';
    $.post(url, obj, function(data){
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
        send_listacotejo();
    });
    // $('button').button();
});
