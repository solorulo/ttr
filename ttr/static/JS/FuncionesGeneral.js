function iniciaEscuela(id,nivel){
	window.location.href="/indexInter/?id="+id+"&niv="+nivel;
}

function cargaError(){

        var objBoton='<%=btnError.ClientID%>'

        if({{error}}.length!=0)
            objBoton.click();
        }