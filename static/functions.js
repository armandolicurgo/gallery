// function.js ;



var req;
 
function likePhoto(valor) {
 
// Verificando Browser;
if(window.XMLHttpRequest) {
   req = new XMLHttpRequest();
}
else if(window.ActiveXObject) {
   req = new ActiveXObject("Microsoft.XMLHTTP");
}
 
var url = "/like/"+valor;
 req.open("Get", url, true);


 
// Quando o objeto recebe o retorno, chamamos a seguinte função;
req.onreadystatechange = function() {
 
	if(req.readyState == 1) {
		var nada;
	}
 
	// Verifica se o Ajax realizou todas as operações corretamente
	if(req.readyState == 4 && req.status == 200) {
 
	// Resposta retornada pelo busca.php
	var resposta = req.responseText;
 
	// Abaixo colocamos a(s) resposta(s) na div resultado
	document.getElementById('re'+valor).innerHTML = resposta;

	}
}
req.send(null);
}

 
function approvePhoto(valor) {
 
// Verificando Browser
if(window.XMLHttpRequest) {
   req = new XMLHttpRequest();
}
else if(window.ActiveXObject) {
   req = new ActiveXObject("Microsoft.XMLHTTP");
}
 
var url = "/approve/"+valor;
 req.open("Get", url, true);
 
// Quando o objeto recebe o retorno, chamamos a seguinte função;
req.onreadystatechange = function() {
 
	// Exibe a mensagem "Buscando Noticias..." enquanto carrega;
	if(req.readyState == 1) {
		document.getElementById('resultado').innerHTML = 'Buscando Noticias...';
	}
 
	// Verifica se o Ajax realizou todas as operações corretamente;
	if(req.readyState == 4 && req.status == 200) {
 
	// Resposta retornada pelo busca.php
	var resposta = req.responseText;
 
	// Abaixo colocamos a(s) resposta(s) na div resultado
	//document.getElementById('resultado').innerHTML = resposta;
	}
}
req.send(null);
}

 
function disapprovePhoto(valor) {
 
// Verificando Browser
if(window.XMLHttpRequest) {
   req = new XMLHttpRequest();
}
else if(window.ActiveXObject) {
   req = new ActiveXObject("Microsoft.XMLHTTP");
}
 
var url = "/disapprove/"+valor;
 req.open("Get", url, true);
 
// Quando o objeto recebe o retorno, chamamos a seguinte função;


req.onreadystatechange = function() {
 
	// Exibe a mensagem "Buscando Noticias..." enquanto carrega
	if(req.readyState == 1) {
		document.getElementById('resultado'+valor).innerHTML = '...';
	}
 
	// Verifica se o Ajax realizou todas as operações corretamente
	if(req.readyState == 4 && req.status == 200) {
 
	// Resposta retornada pelo busca.php
	var resposta = req.responseText;
 
	// Abaixo colocamos a(s) resposta(s) na div resultado
	document.getElementById('resultado'+valor).innerHTML = resposta;
	}
}
req.send(null);
}

