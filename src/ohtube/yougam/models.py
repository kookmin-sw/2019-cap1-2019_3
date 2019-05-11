from django.db import models
from django.utils import timezone
import random
# # Create your models here.

class Video(models.Model):
   url = models.CharField(max_length=255,default="")
   sentiment_neutral = models.IntegerField(default=0)
   sentiment_happy = models.IntegerField(default=0)
   sentiment_sad = models.IntegerField(default=0)
   sentiment_surprise = models.IntegerField(default=0)
   sentiment_anger = models.IntegerField(default=0)
   sentiment_fear = models.IntegerField(default=0)

   def __str__(self):
      return self.url

   def generate(self):
      self.save()

class Comment(models.Model):
	video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
	cid = models.CharField(max_length=255,default="")
	cmt = models.TextField(default="")
	label  = models.IntegerField(default=3)
	label6 = models.CharField(max_length = 100)
	author = models.CharField(max_length=255,default="")
	period = models.CharField(max_length=255,default="")
	randnum = models.IntegerField(default = 1)
	like = models.IntegerField(default = 1)

	def generate(self):
		self.randnum = random.randrange(1,10)
		self.save()

	def __str__(self):
		return "comment ID: {}, author: {}".format(self.cid, self.cmt)




