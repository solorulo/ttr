var MAX_ROWS = 10;
var MAX_COLUMNS = 5;
var nrows = 2;
var ncolumns = 2;
function update_buttons() {
    if (nrows >= MAX_ROWS) {
        $('#add_row').attr("disabled", true);
    }
    else {
        $('#add_row').removeAttr("disabled");
    }
    if (ncolumns >= MAX_COLUMNS) {
        $('#add_column').attr("disabled", true);
    }
    else {
        $('#add_column').removeAttr("disabled");
    }
}
function add_row() {
    if (nrows >= MAX_ROWS) {
        return;
    }
    ++nrows;
    var $tbody = $('#tbody');
    var id = "row"+nrows;
    var $new_row = $("<tr class=\"row\" id=\""+id+"\"></tr>");

    var $td = $('<td></td>');
    var $button = $("<button class=\"delete_row\" meta:index=\"" + nrows + "\">-</button>");
    $button.click(function(event) {
        event.preventDefault();
        delete_row($(this));
    });
    $td.append($button);
    $td.append("<input name=\"cat[" + nrows + "]\" type=\"text\"/>");

    $new_row.append($td);
    // var content = 
    //     "<tr class=\"row\" id=\""+id+"\">" +
    //         "<td>" +
    //             "<button class=\"delete_row\" meta:index=\"" + nrows + "\">-</button>" +
    //                 "<input name=\"cat[" + nrows + "]\" type=\"text\"/>" +
    //         "</td>";
    for (var i = 1; i <= ncolumns; i++) {
        // content += 
        //     "<td><input name=\"pond_val["+ nrows + "][" + i + "]\" type=\"text\" value=\"4\" /></td>";
        $new_row.append("<td><input name=\"pond_val["+ nrows + "][" + i + "]\" type=\"text\" value=\"4\" /></td>");
    }
    // content += 
    //     "</tr>";
    $tbody.append($new_row);
    update_buttons();
}
function add_column(){
    if (ncolumns >= MAX_COLUMNS) {
        return;
    }
    ++ncolumns;
    var $tbody = $('#tbody');
    var $ac_cont = $('#ac_cont');
    var $new_colh = $('<th></th>');
    $new_colh.append("<input name=\"pond[" + ncolumns + "]\" type=\"text\" value=\"4\" />");
    var $bt_delete_column = $("<button id=\"delete_column[" + ncolumns + "]\">-</button>");
    $new_colh.append($bt_delete_column);
    
    $new_colh.insertBefore($ac_cont);
    $('.row').each(function(idx, val){
        var $td = $('<td></td>');
        $td.append("<input name=\"pond_val["+ nrows + "][" + ncolumns + "]\" type=\"text\" value=\"4\" />");
        $(this).append($td);
    });
    update_buttons();
}
function delete_row($obj) {
    var element_id = $obj.attr("meta:index");
    $('#row'+element_id).remove();
    update_buttons();
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
        delete_row($(this));
    });
});
