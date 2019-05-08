from django import forms
from .models import Video

class PostForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('url',)
