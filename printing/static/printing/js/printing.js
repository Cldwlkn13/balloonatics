$(document).ready(function () {
    // submit the form if passes client side validation
    $('#submit-btn').click(function (ev) {
        var message = $('input[name="custom_message"]').val();
        var qty = $('input[name="qty"]').val();
        var form = $('#order-form');
        if (validator(message, qty) == 'ok') {
            form.submit();
        } else {
            ev.preventDefault();
            return;
        }
    });

    // update form with selected balloon & highlight its border
    $('.print-card-select').click(function () {
        var thisid = $(this).children('p').first().text();
        $('.border-success').removeClass('border-success border-3');
        $(this).parent().addClass('border-success border-3');
        $('input[name="p_id"]').val() = thisid;
    })

    // on load highlight selected balloon border if in update mode
    $('.print-card-select').each(function (index) {
        var id = $(this).children('p').first().text();
        var selectedid = $('input[name="p_id"]').val();
        $(this).parent().toggleClass('border-success border-3', id == selectedid);
    })

    // custom message input validation
    $('input[name="custom_message"]').on('input', function (e) {
        var message = $('input[name="custom_message"]').val();
        var valid = validator(message);
        if (valid == 'ok') {
            $('#step-2').html(`<p> 2. Add your message <i class="fas fa-check text-success"></i></p>`)
        } else {
            $('#step-2').html(`<p> 2. Add your message <span class="text-danger"><small>${valid}<small></span></p>`);
        }
    });

    //slideshow controls
    $('#slideshow').hide();
    $('#slideshow-toggle').click(function () {
        var visible = $('#slideshow').is(":visible");
        $('#slideshow').fadeToggle(500);
        if (visible) {
            $(this).html(`<span>&#x25BC; Show me some cool custom print ideas</span>`)
        } else {
            $(this).html(`<span>&#x25B2; Hide Slideshow</span>`)
        }
    });

    // update the total price on form input change event
    $('#order-form').find('input').on('change', function (e) {
        updateTotalPrice();
    });

    // custom form validation 
    function validator(message, qty = 1) {
        if (typeof message == 'undefined') {
            return 'undefined'
        }
        if (message.startsWith(' ')) {
            return 'Message cannot start with a blank space';
        }
        if (message.length < 1) {
            return 'Please add a message';
        }
        if (message.length > 40) {
            return 'Message is too long. 40 characters max.';
        }
        if (qty < 1) {
            return 'Invalid Quantity Selected';
        }
        return 'ok';
    };

    //updated price handler
    function updateTotalPrice() {
        var message = $('input[name="custom_message"]').val();
        var valid = validator(message);
        if (valid == 'ok') {
            getTotalPrintPrice(function (output) {
                var html = `€${output}`
                $('#print-total-price').text(html);
            });
        } else {
            var html = 'n/a';
            $('#print-total-price').text(html);
        };
    }
    updateTotalPrice();

    //ajax call to server for updated price
    function getTotalPrintPrice(handleData) {
        var form = $('#order-form')
        var data = $(form).serialize();
        var url = '/printing/gettotalprice/'

        $.post({
            url: url,
            data: data,
            success: function (response) {
                handleData(response);
            },
            error: function () {
                handleData(response);
            }
        });
    }
})