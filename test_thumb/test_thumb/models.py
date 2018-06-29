from django.db import models
from thumb import VideoThumbnailField, ImageThumbnailField


class VideoMedia(models.Model):
    video = models.FileField()
    thumbnail = VideoThumbnailField()

class ImageMedia(models.Model):
    thumbnail = ImageThumbnailField()
