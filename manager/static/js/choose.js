document.addEventListener("DOMContentLoaded", function() {
	var optns = document.querySelectorAll("#id_product option")

	for(var i = 0; i < optns.length; i++){
		console.log(optns[i])
	}
});