from products.models import Category, Sub_Category


def menu_context(request):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()

    menu_context = {
        'categories': categories,
        'sub_categories': sub_categories,
    }

    return {'menu_context': menu_context}
