from django import forms
from django.forms import formset_factory

from .models import Bundle, BundleItem
from products.models import Product


class BundleSelectorForm(forms.Form):
    bundles = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bundles = Bundle.objects.all()
        self.fields['bundles'].choices = self._load_choices(
            bundles)

    def _load_choices(self, products):
        choices = [(0, 'Select a bundle to edit...')]
        for p in products:
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
        self.fields['product'].choices = product_names
        self.fields['item_qty'].initial = 1
        for field in self.fields.values():
            field.label = ''

BundleFormset = formset_factory(
    form=BundleBuilderForm, extra=1
)
