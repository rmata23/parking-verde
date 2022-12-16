$(document).ready(function(){
	
	function salida(){
		$.ajax({
			url:'/Salida',
			data: $('form'),
			type: 'POST',
			success:function(response){
				
				Alert("Se ha registrado la entrada, por favor guarda tu codigo")
			},
			error:function(error){
				console.log(error);
			}
		});
	}
	function bBuscar(){
		$.ajax({
			url:'/salida',
			data: $('form').serialize(),
			type: 'POST',
			success:function(response){
				location.href='/salida/'+document.getElementById("#CodigoE").value
				
			},
			error:function(error){
				console.log(error);
			}
		});
	}
	
	$("#salida-form1").submit(function(event){
		event.preventDefault();
		
	});
	
});