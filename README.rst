=====
django-thumb
=====

django-thumb is a simple Django app contains 2 models fields 
to generate images from videos and write on images

Visit the github repo https://github.com/AmrAnwar/django-thumb  for more info.

Quick start
-----------

1. Add "thumb" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'thumb',
    ]

2. Add the STATIC_ROOT, MEDIA_ROOT and MEDIA_URL in setting like:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = 'media'
    MEDIA_URL = '/media/'

3. Add the MEDIA path to your urlpatterns in urls.py like:
    ...
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
        ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

3. Run `python manage.py collectstatic ` to create the static fields in your root.

4. now you can use the app model fields like:
    from thumb import ImageThumbnailField, VideoThumbnailField

5. in VideoThumbnailField you have to give the video field name if it's not named as `video`:
    my_video = models.FileField()
    thumb = VideoThumbnailField(video_field_name="my_video")

6. test the Thumbnail Fields in the admin page http://127.0.0.1:8000/admin/
   

### Visit https://github.com/AmrAnwar/django-thumb for more info.