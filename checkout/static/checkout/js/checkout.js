$(document).ready(function() {
    var proceed = $('input[name="proceed"]').val();
    var isTrueSet = (proceed === 'true');
    $('#stripe-fieldset').toggle(isTrueSet); 
    $('#pre-submit-btn').toggle(!isTrueSet);
    $('#card-element').focus();   
    scrollTo($('#card-element'));

    $('#customer-fieldset').find('input').each(function(e) {
        $(this).prop('disabled', isTrueSet);
    })

    $('#address-fieldset').find('input').each(function(e) {
        $(this).prop('disabled', isTrueSet);    
    })

    // scroll to the new row added
    // https://stackoverflow.com/questions/6677035/jquery-scroll-to-element
    function scrollTo(elem) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $(elem).offset().top - 100
        }, 1000);
    };
})