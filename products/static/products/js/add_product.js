$(document).ready(function () {
    
    
    var elem = $('input[name="is_bundle"]');
    var checked = $(elem).prop("checked");
    $('#div_id_bundle_items').toggle(checked);

    $('input[name="is_bundle"]').change(function () {
        var elem = $('input[name="is_bundle"]')
        var checked = $(elem).prop("checked")
        $('#div_id_bundle_items').toggle(checked)
    });


});