from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from orders.models import Cart

@receiver(post_save, sender=User)
def create_user_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        # Créer le profil utilisateur
        UserProfile.objects.create(user=instance)
        # Créer le panier
        Cart.objects.create(user=instance)
