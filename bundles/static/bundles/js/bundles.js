$(document).ready(function () {
    
    // BUNDLES.html
    // toggle the age selector if cat birthday selected
    $('#div_id_age').toggle(
        $('select[name="categories"] option:selected').text().toLowerCase() == 'birthday'
    )

    // trigger the selector form submit if age selector not available
    $('select[name="categories"]').on('change', function (e) {
        if ($(this).find(":selected").text().toLowerCase() != 'birthday') {
            $('#selector-form').find('button').first().trigger('click');
        } else {
            $('#div_id_age').toggle($(this).find(":selected").text().toLowerCase() == 'birthday')
        }
    });

    // trigger the selector form submit if age selector available
    $('select[name="age"]').on('change', function (e) {
        $('#selector-form').find('button').first().trigger('click');
    });

    // toggle the slideshow
    $('#slideshow').hide();
    $('#slideshow-toggle').click(function () {
        var visible = $('#slideshow').is(":visible");
        $('#slideshow').fadeToggle(500);
        if (visible) {
            $(this).html(`<span>&#x25BC; Show me some cool bundles</span>`)
        } else {
            $(this).html(`<span>&#x25B2; Hide Slideshow</span>`)
        }
    });
    
    
    //WITH_ITEMS.html
    // on load get all the product images for the components of the bundle
    $('#item-formset').find('select').each(function (index) {
        getImage(function (output) {
            $('#img-' + index).attr("src", output);
        }, this.value);
    });

    // on load toggle the row on the validity of the loaded value in the select 
    // e.g. when bundle loads and item has 0 qty_held we dont't want to see it 
    $('#item-formset').find('.formset-row').each(function (index) {
        $(this).toggle($('#formset-row-' + index).find('select').first().prop('selectedIndex') != 0);
    });

    // on load toggle the img displayed on the validity of the loaded value in the select
    $('#item-formset').find('img').each(function (index) {
        $(this).toggle($('#formset-row-' + index).find('select').first().prop('selectedIndex') != 0);
    });

    // when component product updated then get that product img and update bundle price 
    $('#item-formset').find('select').on('change', function (e) {
        var selected = $(this).attr('name').split('-')[1];
        var row = $('#formset-row-' + selected);
        $(row).find('.cart-img').toggle($(this).prop('selectedIndex') != 0);
        if (this.value != 0) {
            getImage(function (output) {
                $('#img-' + selected).attr("src", output);
            }, this.value);
        }
        updateBundlePrice(function (output) {
            var html = `€${output}`
            $('#bundle-total-price').text(html);
        });
    });

    // perform clone row when add row btn clicked
    $('.add-form').on('click', function (e) {
        var formsCount = $('.formset-row').length;
        cloneRow($('.formset-row').first(), formsCount);
    });

    // perform remove row when remove row btn clicked
    $('.remove-form').on('click', function (e) {
        var i = $(this).attr('id').split('-')[1];
        removeRow(i);
        updateBundlePrice(function (output) {
            var html = `€${output}`
            $('#bundle-total-price').text(html);
        });
    });

    // when component qty updated then get that product img and update bundle price 
    $('#item-formset').find('input').on('change', function (e) {
        if ($(this).val() < 1) {
            $(this).val(1);
        }
        updateBundlePrice(function (output) {
            var html = `€${output}`
            $('#bundle-total-price').text(html);
        });
    });

    // ajax call to backend to get img
    function getImage(handleData, p_id) {
        if (p_id == 0) {
            return;
        }
        $.get({
            url: '/products/serveimage/' + p_id,
            success: function (response) {
                handleData(response);
            },
            error: function () {
                handleData(response);
            }
        });
    }

    // ajax call to backend to get the updated price
    function updateBundlePrice(handleData) {
        var form = $('#item-formset')
        var data = $(form).serialize();
        var url = '/bundle/gettotalprice/'

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

    // clone the row to be added to at the bottom of the form
    function cloneRow(selector, formsCount) {
        var newRow = $(selector).clone(true);
        $(newRow).attr('id', 'formset-row-' + formsCount);
        $(newRow).show();
        $(newRow).focus();

        var productDiv = newRow.find('#div_id_form-0-product').attr('id', '#div_id_form-' + formsCount + '-product');
        var qtyDiv = newRow.find('#div_id_form-0-item_qty').attr('id', '#div_id_form-' + formsCount + '-item_qty');

        var productSelect = productDiv.find('select').first();
        var qtySelect = qtyDiv.find('input').first();

        $(newRow).find('.cart-img').hide();
        $(newRow).find('img').attr('id', 'img-' + formsCount);
        $(newRow).find('img').attr('src', '');

        $(productSelect).attr('id', 'id_form-' + formsCount + '-product');
        $(productSelect).attr('name', 'form-' + formsCount + '-product');
        $(productSelect).find('option:eq(0)').prop('selected', true);

        $(qtySelect).attr('id', 'id_form-' + formsCount + '-item_qty');
        $(qtySelect).attr('name', 'form-' + formsCount + '-item_qty');
        $(qtySelect).val(1);

        $(newRow).find('#remove-0').attr('id', 'remove-' + formsCount);

        $('.formset-row').last().after(newRow);
        scrollTo(newRow);
    }

    // remove a row 
    function removeRow(i) {
        var row = $('#item-formset').find('#formset-row-' + i);
        $(row).find('select option:eq(0)').prop('selected', true);
        $(row).hide();
    }

    // scroll to the new row added
    // https://stackoverflow.com/questions/6677035/jquery-scroll-to-element
    function scrollTo(elem) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $(elem).offset().top
        }, 1000);
    };
});