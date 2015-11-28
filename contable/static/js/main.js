var j = 2 ;
$('#plus').click(function(){
    for (var i=0; i<2; i++){
        j++ ;
        var form = $('#a').clone() ;
        form.attr({'id' : 'form'+j}) ;
        form.attr({'class' : 'fila'}) ;
        form.find('select').attr({'id' : 'cuenta'+j}) ;
        form.find('select').attr({'name' : 'cuenta'+j}) ;
        form.find('input').attr({'id' : 'monto'+j}) ;
        form.find('input').attr({'name' : 'monto'+j}) ;
        form.appendTo('#'+i+'-cuenta') ;
    }
    $('#counter').attr({'value' : j}) ;
}) ;

$('#less').click(function(){
    for (var i=0; i<2 ; i++){
        var form = $('#form'+j).removeClass('fila');
        form = $('#form'+j).addClass('fila-remove');
        j-- ;
    }
    $('#counter').attr({'value' : j}) ;
}) ;

function obtenerEmpleado(id) {
        $('#nombre').attr({'value' : $('#'+id).find('#nombres').text()}) ;
        $('#horasExtras').attr({'value': $('#'+id).find('#he').text()}) ;
        $('#codigo').attr({'value' : id}) ;
        $('#'+id).addClass('mostrar') ;
}

//$('#form2').clone().appendTo('#'+i+'-cuenta') ;