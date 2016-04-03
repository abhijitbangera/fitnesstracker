from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class basictracker(models.Model):
	weight=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __unicode__(self):
		return self.user
