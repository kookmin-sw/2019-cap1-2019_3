from django.contrib import admin
from .models import Comment
from .models import Video
from .models import ReplyData
from .models import TimeLog

 # Register your models here.
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(ReplyData)
admin.site.register(TimeLog)