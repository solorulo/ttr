var COTEJO_MAX_ROWS = 10;
function add_row() {
    // if ($('.row').length >= COTEJO_MAX_ROWS) {
    //     return;
    // }
    // var $tbody = $('#tbody');
    // var $new_row = $("<tr class=\"row\" meta:new=\"true\"></tr>");

    // var $td = $('<td></td>');
    // var $button = $("<button class=\"delete_row\">-</button>").button();
    // $button.click(function(event) {
    //     event.preventDefault();
    //     delete_row($(this));
    // });
    // $td.append($button);
    // $td.append("<input type=\"text\"/ placeholder=\"Categoría\">");

    // $new_row.append($td);
    // $('.column').each(function(idx, val){
    //     $new_row.append("<td><input type=\"text\" value=\"4\" /></td>");
    // });
    // $tbody.append($new_row);
}
function delete_row($obj) {
    // var parentRow = $obj.parent().parent();
    // parentRow.remove();
}
function send_listacotejo() {
    // var ponderaciones_vals = [];
    // var categorias = [];
    // var ponderaciones = [];
    // $('.column').each(function(indexPondVal, val){
    //     var meta_index = $(this).attr('meta:index');
    //     var meta_new = $(this).attr('meta:new');
    //     var input_text = $(this).children('input[type=text]').val();
    //     ponderaciones_vals[indexPondVal] = {
    //         'index_pod' : meta_index,
    //         'meta_new' : meta_new,
    //         'text' : input_text
    //     };
    // });
    // $('.row').each(function(indexRow, val){
    //     var $thisRow = $(this);
    //     var cat = $thisRow.find('td .cat').val();
    //     var meta_index_cat = $thisRow.attr('meta:index');
    //     categorias[indexRow] = {
    //         'val' : cat,
    //         'index_cat' : meta_index_cat
    //     };

    //     $thisRow.children('.column_val').each(function(indexPond, val){
    //         var val = $(this).children('input[type=text]').val();
    //         ponderaciones.push ({
    //             'index' : indexPond,
    //             'cat' : indexRow,
    //             'val' : val
    //         });
    //     });
    // });
    // var obj = {
    //     'titulo' : $('#titulo').val(),
    //     'autor' : $('#autor').val(),
    //     'asignatura' : $('#asignatura').val(),
    //     'oficial' : $('#oficial').val(),
    //     'pod_vals[]' : JSON.stringify(ponderaciones_vals),
    //     'cats[]' : JSON.stringify(categorias),
    //     'pods[]' : JSON.stringify(ponderaciones),
    //     "csrfmiddlewaretoken": $.cookie("csrftoken")
    // };
    // $.post('/instrumento/rubrica/agregar', obj, function(data){
    //     if (data == "true")
    //         window.location.href = "/index";
    // });
}
$(document).ready(function() {
    // $('#add_row').click(function(event) {
    //     event.preventDefault();
    //     add_row();
    // });
    // $('#add_column').click(function(event) {
    //     event.preventDefault();
    //     add_column();
    // });
    // $(".delete_row").click(function() {
    //     event.preventDefault();
    //     delete_row($(this));
    // });
    // $(".delete_column").click(function() {
    //     event.preventDefault();
    //     delete_column($(this));
    // });
    // $('#save').click(function(event) {
    //     send_rubrica();
    // });
    // $('button').button();
});
