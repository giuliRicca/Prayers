from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
# Create your models here.


class Profile(models.Model):
    # PASTOR = 1
    # DIACONO = 2
    # LIDER = 3
    # OTRO = 4
    ROLE_CHOICES = (
        ('a', 'pastor'),
        ('b', 'diacono'),
        ('c', 'lider'),
        ('d', 'otro'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',
                              upload_to="profile_images", null=True)
    bio = models.CharField(max_length=350, default='Esta es mi biografia!')
    role = models.CharField(max_length=1,
                            choices=ROLE_CHOICES, null=True, default='c')

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
