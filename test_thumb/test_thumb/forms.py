from django import forms

from .models import ImageMedia, VideoMedia


class ImageMediaForm(forms.ModelForm):

    class Meta:
        model = ImageMedia
        fields = ('thumbnail', )

class VideoMediaForm(forms.ModelForm):

    class Meta:
        model = VideoMedia
        fields = ('video', 'thumbnail', )
