document.addEventListener("DOMContentLoaded", function() {
	var optns = document.querySelectorAll("#id_product option")

//	for(var i = 0; i < optns.length; i++){
//	    optns[i].addEventListener("click", function(){
//			this.classList.toggle('choosen')
//		})
//		console.log(optns[i])
//	}

	for(var i = 0; i < optns.length; i++){
		optns[i].addEventListener("click", function(){
		    var label = this.innerHTML;
		    label = '#'+String(label);
		    var product = document.querySelector(label)
            product.setAttribute('style', 'display:block');
            product.setAttribute('class', 'chosen');

            var del_prod = product.querySelector('span');
            del_prod.addEventListener('click', function(){
                product.setAttribute('style', 'display:none');
                product.removeAttribute('class');
                product.setAttribute('value', '');
                product.querySelector('input').value = 0;

            })
		})

	}
});