from django.db import models
from django.contrib.auth.models import User
from datetime import datetime   


class userprofile_extended(models.Model):
	GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
	GOAL_CHOICES=(('1', 'Weight Loss'),('2', 'Mass Gain'),('3', 'Lean Muscle Gain'),('4', 'Stay Fit'),)
	user = models.OneToOneField(User)
	mobile = models.IntegerField(max_length=10, null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True, blank=True)
	goal=models.CharField(max_length=1, choices=GOAL_CHOICES,null=True, blank=True)
	age=models.IntegerField(max_length=3, null=True, blank=True)
	about=models.CharField(max_length=400,null=True, blank=True)
	image=models.ImageField(null=True,blank=True,default="./avatar.png")
	trainer=models.CharField(max_length=100,null=True, blank=True)
	nutritionist=models.CharField(max_length=100,null=True, blank=True)
	supplimentexpert=models.CharField(max_length=100,null=True, blank=True)
	contact=models.CharField(max_length=100,null=True, blank=True)
	def __str__(self):
		return str(self.user)

class subscription(models.Model):
	user=models.ForeignKey(User)
	user_name=models.CharField(max_length=100,null=True, blank=True)
	subscription_startdate=models.DateTimeField(default=datetime.now(), blank=True)
	expire_days=models.IntegerField(max_length=5, null=True, blank=True)
	subscription_status=models.BooleanField(default=False)
	def __str__(self):
		return str(self.user)
		
class photos(models.Model):
	user=models.ForeignKey(User)
	user_photo=models.ImageField(null=True,blank=True)
	datetime = models.DateTimeField(auto_now_add=True)
	description=models.CharField(max_length=50,null=True, blank=True)
	def __str__(self):
		return str(self.user)

# Create your models here.
class basictracker(models.Model):
	weight=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __str__(self):
		return str(self.user)


class bisceptracker(models.Model):
	biscep=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __str__(self):
		return str(self.user)


class chesttracker(models.Model):
	chest=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __str__(self):
		return str(self.user)


class backtracker(models.Model):
	back=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __str__(self):
		return str(self.user)


class hiptracker(models.Model):
	hip=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __str__(self):
		return str(self.user)


class thightracker(models.Model):
	thigh=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __str__(self):
		return str(self.user)

class shouldertracker(models.Model):
	shoulder=models.IntegerField()
	datetime = models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User)

	def __str__(self):
		return str(self.user)