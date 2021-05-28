from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name


class Material(models.Model):
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name


class Sub_Category(models.Model):

    class Meta:
        verbose_name_plural = 'Sub_Categories'

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    sub_category = models.ForeignKey('Sub_Category', null=True, blank=True,
                                     on_delete=models.SET_NULL)
    material = models.ForeignKey('Material', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    uuid = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False,
                                default=0.00)
    discounted_price = models.DecimalField(max_digits=6, decimal_places=2,
                                           blank=False, default=0.00)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    message = models.CharField(max_length=254, null=True, blank=True)
    is_printable = models.BooleanField(null=False, blank=False)
    age = models.IntegerField(null=True)
    qty_held = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name
