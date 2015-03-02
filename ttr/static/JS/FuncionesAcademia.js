function eliminarAcademia( id ) {
  $.post("/academia/borrar",
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

function consultarAcademia(id){
	window.location.href="/academia/consultar/?id="+id;
}