$(document).ready(function () {
    var quantity = 0;
    $('.quantity-right-plus').click(function (e) {
        console.log(quantity);
        e.preventDefault();
        var quantity = parseInt($(this).parent().siblings('#qty').val());
        $(this).parent().siblings('#qty').first().val(quantity + 1);
    });

    $('.quantity-left-minus').click(function (e) {
        e.preventDefault();
        var quantity = parseInt($(this).parent().siblings('#qty').val());
        if (quantity > 1) {
            $(this).parent().siblings('#qty').first().val(quantity - 1);
        }
    });
});