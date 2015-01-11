function eliminarUsuario( id ) {
  $.post("/usuario/borrar/",
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

function consultarUsuario(id){
	window.location.href="/usuario/consultar/?id="+id;
}