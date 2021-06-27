from django.shortcuts import render
from products.models import Category, Sub_Category


def index(request):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()

    # load up the slideshow images 
    slideshow_images_bundle = {
        'graduation-bundle.jpg': 'Our #1 Graduation Bundle',
        'Wedding_Bundle.png': 'Our #1 Wedding Bundle',
        'happy-21stbundle.jpg': 'Happy 21st!',
    }

    slideshow_images_printing = {
        'print-idea-1.jpg': 'Welcome someone home!',
        'print-idea-2.jpg': 'Say Happy Birthday',
        'print-idea-3.jpg': 'Some cool ideas!',
        'print-idea-4.jpg': 'Say a special Congratulaions!',
    }

    slideshow_images_event = {
        'balloon-arch-blue-white.jpg': 'Balloon Arches!',
        'balloon-store-opening.jpeg': 'Store Openings!',
        'balloon-arch-rainbow.jpg': 'Our Rainbow Arch!',
        'balloon-wall-blue.jpg': 'A great Balloon wall idea',
    }
    
    context = {
        'categories': categories, 
        'sub_cateogories': sub_categories,
        'slideshow_images_bundle': slideshow_images_bundle,
        'slideshow_images_printing': slideshow_images_printing,
        'slideshow_images_event': slideshow_images_event,
    }

    return render(request, 'home/index.html', context)


''' error views '''
def bad_request_view(request, exception):

    context = {
        'exception': exception
    }
    
    return render(request, '400.html', context)

def permission_denied_view(request, exception):

    context = {
        'exception': exception
    }
    
    return render(request, '403.html', context)

def page_not_found_view(request, exception):

    context = {
        'exception': exception
    }
    
    return render(request, '404.html', context)


def error_view(request):
    
    return render(request, '500.html')