from django import forms

from .models import CustomPrintedProduct

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
        model = CustomPrintedProduct
        fields = ('custom_message', 'qty')

    custom_message = forms.Textarea()

    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['custom_message'].initial = message


    
