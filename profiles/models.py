from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cust_name = models.CharField(max_length=50, null=True, blank=True)
    cust_email = models.EmailField(max_length=254, null=True, blank=True)
    cust_phone = models.CharField(max_length=20, null=True, blank=True)
    street_address_1 = models.CharField(
        max_length=100, null=True, blank=True)
    street_address_2 = models.CharField(
        max_length=100, null=True, blank=True)
    city_town = models.CharField(
        max_length=20, null=True, blank=True)
    county_area = models.CharField(
        max_length=20, null=True, blank=True)
    country = CountryField(
       blank_label='Country *', null=True, blank=True)
    postal_code = models.CharField(
        max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.username
