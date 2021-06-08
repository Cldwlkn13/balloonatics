from django import forms
from django.forms import formset_factory

from crispy_forms.helper import FormHelper

from .models import Product, Category, Sub_Category, BundleItem


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('qty_in_bag', 'bundle_items')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        cat_display_names = [(c.id, c.get_display_name()) for c in categories]
        sub_categories = Sub_Category.objects.all()
        sub_cat_display_names = [(
            c.id, c.get_display_name()) for c in sub_categories]
        other_products = Product.objects.filter(is_bundle=False)
        other_product_names = [(p.id, p.name) for p in other_products]

        self.fields['category'].choices = cat_display_names
        self.fields['sub_category'].choices = sub_cat_display_names
        # self.fields['bundle_items'].choices = other_product_names


class ProductSelectorForm(forms.Form):
    select_product = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        products = Product.objects.all()
        self.fields['select_product'].choices = self._load_choices(
            products)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    def _load_choices(self, products):
        choices = [(0, 'Select a product to edit...')]
        for p in products:
            choices.append((str(p.id), str(p.name)))
        return choices


class BundleBuilderForm(forms.ModelForm):
    class Meta:
        model = BundleItem
        fields = ('product', 'qty')

    product = forms.ChoiceField()
    qty = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        products = Product.objects.filter(is_bundle=False)
        product_names = [(p.id, p.name) for p in products]
        self.fields['product'].choices = product_names
        self.fields['qty'].initial = 1
        for field in self.fields.values():
            field.label = ''

BundleFormset = formset_factory(
    form=BundleBuilderForm, extra=1
)

