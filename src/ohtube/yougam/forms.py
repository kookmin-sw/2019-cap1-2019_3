from django import forms
from .models import Video

class PostForm(forms.ModelForm):
    url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter a link to YouTube.','size':40}))

    class Meta:
        model = Video
        fields = ('url',) 
