from django import forms
from django.forms import formset_factory

from .models import BundleItem, BundleCategory
from products.models import Product


class BundleSelectorForm(forms.Form):
    categories = forms.ChoiceField()
    age = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = BundleCategory.objects.all()
        self.fields['categories'].choices = self._load_choices(
            categories, 'Select a category...')
        ages = [(_, _) for _ in range(100)]
        self.fields['age'].choices = ages
        self.fields['age'].choices[0] = (0, 'Age')
        for field in self.fields.values():
            field.label = ''

    def _load_choices(self, arr, placeholder):
        choices = [(0, placeholder)]
        for p in arr:
            choices.append((str(p.id), str(p.name)))
        return choices


class BundleBuilderForm(forms.ModelForm):
    class Meta:
        model = BundleItem
        fields = ('product', 'item_qty')

    product = forms.ChoiceField()
    item_qty = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        products = Product.objects.all()
        product_names = [(p.id, p.name) for p in products]
        product_names.insert(0, (0, 'Select a product...'))
        print(product_names)
        self.fields['product'].choices = product_names
        self.fields['item_qty'].initial = 1
        for field in self.fields.values():
            field.label = ''

BundleFormset = formset_factory(
    form=BundleBuilderForm, extra=1
)
