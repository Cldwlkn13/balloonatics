$(document).ready(function () {
    document.getElementById('div_id_select_product').getElementsByTagName('label')[0].style.display = 'none';
    $('#id_image').addClass('btn btn-info mt-1 rounded-3');
    $('#id_select_product').change(function () {
        $('#selector-form').find('button').first().trigger('click');
    });
});