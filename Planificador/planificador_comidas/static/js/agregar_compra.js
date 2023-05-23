$(document).ready(function() {
    var formularioElementos = $('.elemento-container');
    var botonAgregarElemento = $('#agregar-elemento-btn');
    var index = 1;
  
    botonAgregarElemento.on('click', function() {
      var nuevoElemento = formularioElementos.first().clone();
      nuevoElemento.find('input').each(function() {
        $(this).attr('name', $(this).attr('name').replace('0', index));
        $(this).val('');
      });
  
      formularioElementos.last().after(nuevoElemento);
      index++;
    });
  });
  