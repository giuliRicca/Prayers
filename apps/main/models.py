from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Prayer(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=100, null=True)
	body = models.CharField(max_length=500, null=True)
	private = models.BooleanField(default=False)
	created = models.DateField(auto_now=True)

	def __str__(self):
		return self.title

