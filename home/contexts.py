from products.models import Product, Category, Sub_Category
from django.conf import settings


def menu_context(request):

    categories = Category.objects.all()

    menu_context = {}

    for c in categories:
        sub_category_pks = []
        matching_sub_categories = Product.objects.filter(
            category__name=c.name).distinct().values('sub_category')

        sub_category_pks = []
        for msc in matching_sub_categories:
            for v in msc.values():
                sub_category_pks.append(v)

        sub_categories_q = list(Sub_Category.objects.filter(
            id__in=sub_category_pks).values('name'))

        sub_categories = []
        for sc in sub_categories_q:
            for v in sc.values():
                sub_categories.append(v)

        menu_context[c.name] = sub_categories

    return {
        'menu_context': menu_context
        }


def configure_toasts(request):

    toast_delay = settings.TOAST_DELAY
    toast_autohide = settings.TOAST_AUTOHIDE

    return {
        'toast_delay': toast_delay,
        'toast_autohide': toast_autohide
    }
