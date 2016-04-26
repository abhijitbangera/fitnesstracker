from django.db import models
from django.contrib.auth.models import User

class userprofile_extended(models.Model):
	GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
	GOAL_CHOICES=(('1', 'Weight Loss'),('2', 'Mass Gain'),('3', 'Lean Muscle Gain'),('4', 'Stay Fit'),)
	user = models.OneToOneField(User)
	mobile = models.IntegerField(max_length=10, null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True, blank=True)
	goal=models.CharField(max_length=1, choices=GOAL_CHOICES,null=True, blank=True)
	age=models.IntegerField(max_length=3, null=True, blank=True)


# Create your models here.
class basictracker(models.Model):
	weight=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __unicode__(self):
		return self.user

class bisceptracker(models.Model):
	biscep=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __unicode__(self):
		return self.user

class chesttracker(models.Model):
	chest=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __unicode__(self):
		return self.user

class backtracker(models.Model):
	back=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __unicode__(self):
		return self.user

class hiptracker(models.Model):
	hip=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __unicode__(self):
		return self.user

class thightracker(models.Model):
	thigh=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __unicode__(self):
		return self.user