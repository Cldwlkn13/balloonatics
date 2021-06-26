$('input[type="number"]').on('change', function(){
    if($(this).val() < 1) {
        $(this).val(1);
    }
});