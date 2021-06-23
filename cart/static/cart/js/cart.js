$(document).ready(function () {
    // custom script to handle product qtys in the cart with qty widget
    $('.quantity-right-plus').click(function (e) {
        e.preventDefault();
        $(this).parent().siblings('#qty').first().trigger('change');
    });

    $('.quantity-left-minus').click(function (e) {
        e.preventDefault();
        $(this).parent().siblings('#qty').first().trigger('change');
    });

    $('input').on('change', function () {
        console.log($(this));
        $(this).siblings('#update-qty').first().trigger('click');
    });
});