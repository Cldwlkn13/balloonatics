from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('cust_name', 'cust_email', 'cust_phone',
                  'street_address_1', 'street_address_2', 'city_town',
                  'county_area', 'country', 'postal_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'cust_name': 'Default Full Name',
            'cust_email': 'Default Email Address',
            'cust_phone': 'Default Phone Number',
            'street_address_1': 'Default Address 1',
            'street_address_2': 'Default Address 2',
            'city_town': 'Default Your Town or City',
            'county_area': 'Default County or Locality',
            'postal_code': 'Default Post/Zip Code'
        }

        self.fields['cust_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False