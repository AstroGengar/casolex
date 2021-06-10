$(document).ready(function() {
    $("#contact-form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3
            },
            apellido: {
                required: true,
                minlength: 3
            },
            email: {
                required: true,
                email: true
            },
            contrasena: {
                required: true,
                minlength: 5
            }
        }
    });
});


const form = document.getElementById("contact-form");

form.addEventListener("submit", function(event) {
    event.preventDefault();
    var nombre = $('#nombre').val();
    var apellido = $('#apellido').val();
    var email = $('#email').val();
    var contrasena = $('#contrasena').val();
    var checkTerms = $('#checkTerms').is(':checked');

    if (nombre != "" && apellido != "" && email != "" && contrasena != "") {
        if (!checkTerms) {
            alert("Acepte terminos y condiciones");
        } else {
            alert("Formulario enviado");
        }
    } else {
        alert("Por favor complete el formulario.");
    }

})