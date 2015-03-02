function eliminarAsignatura( id ) {
  $.post("/asignatura/borrar",
    {
      "id":id,
      "csrfmiddlewaretoken": $.cookie("csrftoken")
    },
    function(data){
      if (data == "true") {
      	reloadJtree();
      }
    });
}

function consultarAsignatura(id){
	window.location.href="/asignatura/consultar/?id="+id;
}