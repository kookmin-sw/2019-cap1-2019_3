from django.db import models
from django.utils import timezone
import random
# # Create your models here.

class Video(models.Model):
   url = models.CharField(max_length=255,default="")
   title = models.CharField(max_length=255,default="")
   sentiment_neutral = models.IntegerField(default=0)
   sentiment_happy = models.IntegerField(default=0)
   sentiment_sad = models.IntegerField(default=0)
   sentiment_surprise = models.IntegerField(default=0)
   sentiment_anger = models.IntegerField(default=0)
   sentiment_fear = models.IntegerField(default=0)

   def __str__(self):
      return str(self.id)

   def generate(self):
      self.save()

class Comment(models.Model):
	video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
	cid = models.CharField(max_length=255,default="")
	cmt = models.TextField(default="")
	label  = models.IntegerField(default=3)
	label6 = models.CharField(max_length = 100, default="")
	author = models.CharField(max_length=255,default="")
	period = models.CharField(max_length=255,default="")
	randnum = models.IntegerField(default = 1)
	like = models.IntegerField(default = 0)

	def generate(self):
		self.save()

	def __str__(self):
		return str(self.id)


class ReplyData(models.Model):
	video = models.IntegerField(default=-1)
	parent_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
	comment = models.TextField(default="")
	pid = models.CharField(max_length=255,default="")
	label  = models.IntegerField(default=3)
	label6 = models.CharField(max_length = 100)
	author = models.CharField(max_length = 255)
	period = models.CharField(max_length = 255)
	like = models.IntegerField(default = 0)
	randnum = models.IntegerField(default = 1)

	def generate(self):
		self.save()

	def __str__(self):
		return self.comment


class TimeLog(models.Model):
   top_sentiment = models.CharField(max_length = 255)
   url = models.CharField(max_length=255)
   time = models.CharField(max_length = 255)
   img_path = models.ImageField()

   def __str__(self):
      return str(self.url)

   def generate(self):
      self.save()


class PieChart(models.Model):
	video_id = models.CharField(max_length = 100)
	json_data = models.CharField(max_length = 400)

	def __str__(self):
		return "video_id: {}".format(self.video_id)

	def generate(self):
		self.save()

class WebCam(models.Model):
	video_id = models.CharField(max_length=100)
	json_data = models.CharField(max_length=400)
	video_path = models.CharField(max_length=400, default='SOME STRING')
	capture_path = models.CharField(max_length=400, default='SOME STRING')

	def __str__(self):
		return "video_id: {}".format(self.video_id)

	def generate(self):
		self.save()