$(document).ready(function() {
    $("#form-login").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 4
            },
            contrasena: {
                required: true,
                minlength: 5
            }
        },
        messages: {
            nombre: {
                minlength: "El nombre debe tener al menos 4 caracteres"
            },
            contrasena: {
                contrasena: "Debe tener al menos 5 caracteres"
            }
        }
    });
});


const form = document.getElementById("form-login");

form.addEventListener("submit", function(event) {
    event.preventDefault();
    var nombre = $('#nombre').val();
    var contrasena = $('#contrasena').val();
    if (nombre != "" && contrasena != "") {
        alert("A ingresado exitosamente");

    } else {
        alert("Por favor rellene todos los campos.");
    }
})