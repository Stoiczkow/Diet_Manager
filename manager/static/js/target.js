document.addEventListener("DOMContentLoaded", function() {
    var btns = document.querySelectorAll(".targets");
    var inputs = document.querySelectorAll("input");

    for(var i = 0; i < btns.length; i++){
        btns[i].addEventListener("click", function(){
            var target_data = this.getAttribute("data").split(",");
            for(var j = 1; j < inputs.length; j++){
                inputs[j].value = target_data[j - 1];
            };
        });
    };
});