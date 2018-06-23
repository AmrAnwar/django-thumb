from django.db import models

from .form_field import ImageThumbnailFieldForm


class ImageThumbnailField(models.ImageField):

    def formfield(self, *args, **kwargs):
        return super(ImageThumbnailField, self).formfield(
            form_class=ImageThumbnailFieldForm,
            **kwargs)
