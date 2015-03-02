function eliminarUsuario( id ) {
  $.post("/usuario/borrar/",
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

function consultarUsuario(id){
	window.location.href="/usuario/consultar/?id="+id;
}