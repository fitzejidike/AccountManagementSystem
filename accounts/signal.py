from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Account
from user.models import User


@receiver(post_save, sender=User)
def create_profile(created, instance, **kwargs):
    if created:
        Account.objects.create(user=instance,
                               accounts_number=instance.phone[1:]
                               )
