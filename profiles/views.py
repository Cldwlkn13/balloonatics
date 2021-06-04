from django.shortcuts import (render, redirect, reverse)
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import ProfileForm


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form_data = {
            'cust_name': request.POST['cust_name'],
            'cust_email': request.POST['cust_email'],
            'cust_phone': request.POST['cust_phone'],
            'street_address_1': request.POST['street_address_1'],
            'street_address_2': request.POST['street_address_2'],
            'city_town': request.POST['city_town'],
            'county_area': request.POST['county_area'],
            'country': request.POST['country'],
            'postal_code': request.POST['postal_code'],
        }
        profile_form = ProfileForm(profile_form_data)
        if profile_form.is_valid():
            try:
                profile = UserProfile.objects.get(user=request.user)
                profile.update(
                    cust_name=profile_form_data['cust_name'],
                    cust_email=profile_form_data['cust_email'],
                    cust_phone=profile_form_data['cust_phone'],
                    street_address_1=profile_form_data['street_address_1'],
                    street_address_2=profile_form_data['street_address_2'],
                    city_town=profile_form_data['city_town'],
                    county_area=profile_form_data['county_area'],
                    country=profile_form_data['country'],
                    postal_code=profile_form_data['postal_code'])

                messages.success(request,
                                 "Your profile has been saved!",
                                 extra_tags='render_toast')

                orders = profile.orders.all()
                context = {
                    'profile': profile,
                    'profile_form': profile_form,
                    'orders': orders
                }
                return render(request, 'profiles/profile.html', context)

            except UserProfile.DoesNotExist:
                messages.error(request,
                           "Error saving your profile!",
                           extra_tags='render_toast')
                return redirect(reverse('profile'))

        else:
            messages.error(request,
                           "Error saving your profile!",
                           extra_tags='render_toast')
            return redirect(reverse('profile'))
                       
    else:
        profile = UserProfile.objects.get(user=request.user)
        profile_form = ProfileForm(instance=profile)
        orders = profile.orders.all()

        context = {
            'profile': profile,
            'profile_form': profile_form,
            'orders': orders
        }

    return render(request, 'profiles/profile.html', context)