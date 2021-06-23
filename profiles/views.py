from django.shortcuts import (render, redirect, reverse)
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import ProfileForm


@login_required
def profile(request):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            try:
                profile_form.save()
                messages.success(request,
                    "Your profile has been saved!",
                    extra_tags='render_toast')

                context = {
                    'profile_form': profile_form,
                }
                return redirect(reverse('profile'))

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
        orders = profile.orders.all().order_by('-date')

        context = {
            'profile': profile,
            'profile_form': profile_form,
            'orders': orders
        }

    return render(request, 'profiles/profile.html', context)