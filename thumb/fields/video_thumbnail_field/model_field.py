from django.db import models

from .form_field import VideoThumbnailFieldForm


class VideoThumbnailField(models.ImageField):

    def __init__(self, video_field_name="video", *args, **kwargs):
        self.video_field_name = video_field_name
        super(VideoThumbnailField, self).__init__(*args, **kwargs)

    def formfield(self, *args, **kwargs):
        return super(VideoThumbnailField, self).formfield(
            form_class=VideoThumbnailFieldForm,
            video_field_name=self.video_field_name,
            **kwargs)
