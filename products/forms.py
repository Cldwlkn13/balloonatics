from django import forms
from crispy_forms.helper import FormHelper

from .models import Product, Category, Sub_Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('qty_in_bag',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        cat_display_names = [(c.id, c.get_display_name()) for c in categories]
        sub_categories = Sub_Category.objects.all()
        sub_cat_display_names = [(c.id, c.get_display_name()) for c in sub_categories]

        self.fields['category'].choices = cat_display_names
        self.fields['sub_category'].choices = sub_cat_display_names


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
