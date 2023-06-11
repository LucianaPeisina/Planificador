$(document).ready(function() {
  var formularioCompra = $('#compra-form');
  var botonCrearCompra = $('#crear-compra-btn');
  var contenedorElementos = $('.elementos-container');

  botonCrearCompra.on('click', function() {
    formularioCompra.submit();
  });

  contenedorElementos.show();
});
