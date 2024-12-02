from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Certifique-se de criar o perfil apenas se ele não existir
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Apenas salva se o perfil já estiver associado ao usuário
    if hasattr(instance, 'profile'):
        instance.profile.save()
