from django.contrib import admin
from .models import Comment
from .models import Video
from .models import ReplyData

 # Register your models here.
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(ReplyData)