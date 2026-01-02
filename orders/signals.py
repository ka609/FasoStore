from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from users.models import Notification

@receiver(post_save, sender=Order)
def notify_user_new_order(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"Votre commande #{instance.id} a été créée avec succès.",
            type="order"
        )
