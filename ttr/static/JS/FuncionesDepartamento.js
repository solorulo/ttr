function eliminarDepartamento( id ) {
  $.post("/departamento/borrar/",
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

function consultarDepartamento(id){
	window.location.href="/departamento/consultar/?id="+id;
  return false;
}