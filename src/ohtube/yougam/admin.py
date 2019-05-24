from django.contrib import admin
from .models import Comment
from .models import Video
from .models import ReplyData
from .models import TimeLog
from .models import PieChart
from .models import WebCam
from .models import test

 # Register your models here.
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(ReplyData)
admin.site.register(TimeLog)
admin.site.register(PieChart)
admin.site.register(WebCam)
admin.site.register(test)
