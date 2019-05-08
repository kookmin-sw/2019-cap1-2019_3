from django.db import models
from django.utils import timezone
import random
# # Create your models here.

class Video(models.Model):
	url = models.CharField(max_length=500,default="")

	def __str__(self):
		return self.url

	def generate(self):
		self.save()

class Comment(models.Model):
	video = models.IntegerField(default=0)
	cid = models.CharField(max_length=255,default="")
	cmt = models.TextField(default="")
	label  = models.IntegerField(default=3)
	author = models.CharField(max_length=255,default="")
	period = models.CharField(max_length=255,default="")
	randnum = models.IntegerField(default = 1)

	def generate(self):
		self.randnum = random.randrange(1,10)
		self.save()




