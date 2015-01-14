function eliminarDepartamento( id ) {
  $.post("/departamento/delete",
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

function consultarDepartamento(id){
	window.location.href="/departamento/consultar/?id="+id;
}