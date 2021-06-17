
from django import forms

from .models import CustomPrintOrder

from products.models import Product


class ProductSelectorForm(forms.Form):
    select_product = forms.ChoiceField()

    def __init__(self, selected, *args, **kwargs):
        super().__init__(*args, **kwargs)
        products = Product.objects.filter(is_printable=True)
        self.fields['select_product'].choices = self._load_choices(
            products)
        self.fields['select_product'].initial = selected

    def _load_choices(self, products):
        choices = [(0, 'Select a product')]
        for p in products:
            choices.append((str(p.id), str(p.name)))
        return choices


class CustomPrintForm(forms.ModelForm):
    class Meta:
        model = CustomPrintOrder
        fields = ('custom_message', 'qty')

    custom_message = forms.CharField(label='Your message')

    def __init__(self, message, qty, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['custom_message'].widget.attrs['placeholder'] = 'Enter your message here'
        self.fields['custom_message'].initial = message
        self.fields['qty'].initial = qty


    
