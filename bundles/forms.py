from django import forms
from django.forms import formset_factory

from .models import BundleItem, BundleCategory
from products.models import Product


class BundleSelectorForm(forms.Form):
    categories = forms.ChoiceField(label='Step 1. Choose a Bundle Category')
    age = forms.ChoiceField(label='For birthday bundles, select a target age')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = BundleCategory.objects.exclude(name='custom')
        self.fields['categories'].choices = self._load_choices(
            categories, '1. What is the occasion?')
        ages = [(_, _) for _ in range(100)]
        self.fields['categories'].label = ''
        self.fields['age'].choices = ages
        self.fields['age'].choices[0] = (0, 'Age')

    def _load_choices(self, arr, placeholder):
        choices = [(0, placeholder)]
        for bc in arr:
            choices.append((str(bc.id), str(bc.name)))
        return choices


class BundleBuilderForm(forms.ModelForm):
    class Meta:
        model = BundleItem
        fields = ('product', 'item_qty')

    product = forms.ChoiceField(label='Balloon')
    item_qty = forms.IntegerField(label='Qty')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        products = Product.objects.filter(
            qty_held__gt=0)
        product_names = [(p.id, p.name) for p in products]
        product_names.insert(0, (0, 'Select a product...'))
        self.fields['product'].choices = product_names
        self.fields['item_qty'].initial = 1

BundleBuilderFormset = formset_factory(
    form=BundleBuilderForm, extra=0
)
