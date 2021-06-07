from django.shortcuts import render

def bundles(request):
    
    context = {}

    return render(request, 'bundles/bundles.html', context)
