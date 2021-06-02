from django import forms
from .models import Order, Address


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('cust_name', 'cust_email', 'cust_phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'cust_name': 'Full Name',
            'cust_email': 'Email Address',
            'cust_phone': 'Phone Number',
        }

        self.fields['cust_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street_address_1', 'street_address_2', 'city_town',
                  'county_area', 'country', 'postal_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'street_address_1': 'Address 1',
            'street_address_2': 'Address 2',
            'city_town': 'Your Town or City',
            'county_area': 'County or Locality',
            'country': 'Country',
            'postal_code': 'Post/Zip Code'
        }

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
