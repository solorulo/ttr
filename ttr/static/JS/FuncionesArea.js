function eliminarArea( id ) {
  $.post("/area/delete",
    {
      "id":id,
      "csrfmiddlewaretoken": $.cookie("csrftoken")
    },
    function(data){
      if (data == "true") {
      	window.location.reload();
      }
    });
}

function consultarArea(id){
	window.location.href="/area/consultar/?id="+id;
}