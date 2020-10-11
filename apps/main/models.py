from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Prayer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    body = models.CharField(max_length=500, null=True)
    private = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)
    PRAYER_CATEGORIES = [
        ('a', 'salud'),
        ('b', 'familia'),
        ('c', 'espiritualidad'),
        ('e', 'economia'),
        ('d', 'otro'),
    ]
    category = models.CharField(max_length=1,
                                choices=PRAYER_CATEGORIES, null=True, default='a')

    def __str__(self):
        return self.title
