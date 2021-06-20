from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import BundleItem


@receiver(post_save, sender=BundleItem)
def update_on_save(sender, instance, created, **kwargs):
    if instance.bundle:
        instance.bundle.calc_bundle_total()


@receiver(post_delete, sender=BundleItem)
def update_on_delete(sender, instance, **kwargs):
    if instance.bundle:
        instance.bundle.calc_bundle_total()