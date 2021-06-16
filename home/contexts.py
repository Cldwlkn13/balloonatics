from products.models import Product, Category, Sub_Category
from django.conf import settings


def menu_context(request):

    categories = Category.objects.all()

    menu_context = {}

    for c in categories:
        sub_category_pks = []
        matching_sub_categories = Product.objects.filter(
            category__name=c.name).exclude(
                category__name='custom').distinct().values('sub_category')

        for msc in matching_sub_categories:
            for v in msc.values():
                sub_category_pks.append(v)

        sub_categories_q = list(Sub_Category.objects.filter(
            id__in=sub_category_pks).exclude(
                name='custom').values('name'))

        sub_categories = []
        for sc in sub_categories_q:
            for v in sc.values():
                sub_categories.append(v)

        menu_context[c.name] = sub_categories

    return {
            'menu_context': menu_context
        }


def configure_toasts(request):

    if 'toast_autohide' in request.POST:
        toast_autohide = request.POST['toast_autohide']
    else:
        toast_autohide = settings.TOAST_AUTOHIDE

    if 'toast_delay' in request.POST:
        toast_delay = request.POST['toast_delay']
    else:
        toast_delay = settings.TOAST_DELAY

    return {
        'toast_delay': toast_delay,
        'toast_autohide': toast_autohide
    }
