function eliminarAsignatura( id ) {
  $.post("/asignatura/borrar",
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

function consultarAsignatura(id){
	window.location.href="/asignatura/consultar/?id="+id;
}