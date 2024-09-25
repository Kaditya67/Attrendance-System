# myapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Staff, Principal


@receiver(post_save, sender=Staff)
def assign_staff_group(sender, instance, **kwargs):
    group, created = Group.objects.get_or_create(name='Staff')
    instance.user.groups.add(group)

@receiver(post_save, sender=Principal)
def assign_principal_group(sender, instance, **kwargs):
    group, created = Group.objects.get_or_create(name='Principal')
    instance.user.groups.add(group)
