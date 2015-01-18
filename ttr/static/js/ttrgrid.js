var MAX_ROWS = 10;
var MAX_COLUMNS = 5;
function update_buttons() {
    if ($('.row').length >= MAX_ROWS) {
        $('#add_row').attr("disabled", true);
    }
    else {
        $('#add_row').removeAttr("disabled");
    }
    if ($('.column').length >= MAX_COLUMNS) {
        $('#add_column').attr("disabled", true);
    }
    else {
        $('#add_column').removeAttr("disabled");
    }
}
function add_row() {
    if ($('.row').length >= MAX_ROWS) {
        return;
    }
    var $tbody = $('#tbody');
    var $new_row = $("<tr class=\"row\" meta:new=\"true\"></tr>");

    var $td = $('<td></td>');
    var $button = $("<button class=\"delete_row\">-</button>").button();
    $button.click(function(event) {
        event.preventDefault();
        delete_row($(this));
    });
    $td.append($button);
    $td.append("<input type=\"text\"/ placeholder=\"Categoría\">");

    $new_row.append($td);
    $('.column').each(function(idx, val){
        $new_row.append("<td><input type=\"text\" value=\"4\" /></td>");
    });
    $tbody.append($new_row);
    update_buttons();
}
function add_column(){
    if ($('.column').length >= MAX_COLUMNS) {
        return;
    }
    var $tbody = $('#tbody');
    var $new_colh = $('<th class=\"column\" meta:new=\"true\"></th>');
    var $bt_delete_column = $("<button class=\"delete_column\">-</button>").button();
    $bt_delete_column.click(function(event) {
        event.preventDefault();
        delete_column($(this));
    });
    $new_colh.append($bt_delete_column);
    $new_colh.append("<br/><input type=\"text\" value=\"4\" />");
    
    $('#row_header').append($new_colh);
    $('.row').each(function(idx, val){
        var $td = $('<td meta:new=\"true\"></td>');
        $td.append("<input class=\"column_val\" type=\"text\" value=\"4\" />");
        $(this).append($td);
    });
    update_buttons();
}
function delete_row($obj) {
    var parentRow = $obj.parent().parent();
    parentRow.remove();
    update_buttons();
}
function delete_column($obj) {
    // var meta_index = $obj.attr("meta:index");
    // $('.row[meta:index='+meta_index+']').remove();
    var parentTh = $obj.parent();
    var index = parentTh.index() + 1;
    parentTh.remove();
    $(".row :nth-child("+index+")").remove();
    update_buttons();
}
function send_rubrica() {
    var poderaciones_vals = [];
    var categorias = [];
    var ponderaciones = [];
    $('.column').each(function(idx, val){
        var meta_index = $(this).attr('meta:index');
        var meta_new = $(this).attr('meta:new');
        var input_text = $(this).children('input[type=text]').val();
        poderaciones_vals[idx] = {
            'index_pod' : meta_index,
            'meta_new' : meta_new,
            'text' : input_text
        };
    });
    $('.row .cat').each(function(idx1, val){
        var cat = $(this).val();
        var val_cat = {
            'val' : cat
        };
        var parentRow = $(this).parent().parent();
        var meta_index_cat = parentRow.attr('meta:index');
        if (meta_index_cat) {
            val_cat['index_cat'] = meta_index_cat;
        }
        categorias[idx1] = val_cat;

        parentRow.children('.column_val').each(function(idx, val){
            var val = $(this).children('input[type=text]').val();
            ponderaciones[idx] = {
                'cat' : idx1,
                'val' : val
            };
        });
    });
    var obj = {
        'titulo' : $('#titulo').val(),
        'autor' : $('#autor').val(),
        'asignatura' : $('#asignatura').val(),
        'oficial' : $('#oficial').val(),
        'pod_vals[]' : JSON.stringify(poderaciones_vals),
        'cats[]' : JSON.stringify(categorias),
        'pods[]' : JSON.stringify(ponderaciones),
        "csrfmiddlewaretoken": $.cookie("csrftoken")
    };
    $.post('/instrumento/rubrica/agregar', obj, function(data){
        if (data == "true")
            window.location.href = "/index";
    });
}
$(document).ready(function() {
    $('#add_row').click(function(event) {
        event.preventDefault();
        add_row();
    });
    $('#add_column').click(function(event) {
        event.preventDefault();
        add_column();
    });
    $(".delete_row").click(function() {
        event.preventDefault();
        delete_row($(this));
    });
    $(".delete_column").click(function() {
        event.preventDefault();
        delete_column($(this));
    });
    $('#save').click(function(event) {
        send_rubrica();
    });
    $('button').button();
});
