/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements({
    fonts: [
      {
        cssSrc: 'https://fonts.googleapis.com/css2?family=Quicksand:wght@300;500;600&display=swa',
      },
    ],
    locale: window.__exampleLocale
  });
var style = {
    base: {
        color: '#000',
        fontFamily: 'Quicksand',
        fontSmoothing: 'antialiased',
        fontSize: '12px',
        '::placeholder': {
            color: '#aab7c4',
        }
    },
    invalid: {
        color: '#4B0082',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

var form = document.getElementById('payment-form');
$('#submit-button').on('click', function(ev) {
    $('#customer-fieldset').find('input').each(function(e) {
        $(this).prop('disabled', false);
    })

    $('#address-fieldset').find('input').each(function(e) {
        $(this).prop('disabled', false);    
    })
    
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); 
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.cust_name.value),
                    phone: $.trim(form.cust_phone.value),
                    email: $.trim(form.cust_email.value),
                    address:{
                        line1: $.trim(form.street_address_1.value),
                        line2: $.trim(form.street_address_2.value),
                        city: $.trim(form.city_town.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county_area.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.cust_name.value),
                phone: $.trim(form.cust_phone.value),
                address: {
                    line1: $.trim(form.street_address_1.value),
                    line2: $.trim(form.street_address_2.value),
                    city: $.trim(form.city_town.value),
                    country: $.trim(form.country.value),
                    state: $.trim(form.county_area.value),
                    postal_code: $.trim(form.postal_code.value),
                }
            },
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                   form.submit();
                }
            }
        });
    }).fail(function () {
        location.reload();
    })
});


function validateforms(handle, csrfToken) {
    
}