![python version](https://img.shields.io/badge/python-3.4+-blue.svg)
![PyPI - License](https://img.shields.io/pypi/l/Django.svg)

[![PyPI version](https://badge.fury.io/py/django-thumb.svg)](https://badge.fury.io/py/django-thumb)
![coverage](https://svgshare.com/i/7R1.svg)
[![Downloads](http://pepy.tech/badge/django-thumb)](http://pepy.tech/project/django-thumb)

Django-thumb 
=====

**django-thumb is a simple Django app that contains *two models fields* , The app generates images from videos and additionally can create write on images.**

- Quick Preview for `VideoThumbnailField`(Thumbnail)

![testmodel](https://cdn-images-1.medium.com/max/800/1*NiIMKLWMwntViXiJ-5k9og.gif)

###### hope you :star: the repo if you find it helpful

install
-------
```shell
pip install django-thumb # try pip3 if it didn't work
```

Quick setup
-------

1. Add "thumb" to your INSTALLED_APPS setting like this::
```python
    INSTALLED_APPS = [
        ...
        'thumb',
    ]
```
----

##### 2. Add the STATIC_ROOT, MEDIA_ROOT and MEDIA_URL in setting like:

 ```python
	STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = 'media'
    MEDIA_URL = '/media/'
```
----

##### 3. Add the MEDIA path to your urlpatterns in urls.py like:

```python
	....
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
        ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
---

##### 4. Run `python manage.py collectstatic ` to create the static fields in your root.

---

##### 5. now you can use the app model fields like:

```python
from thumb import ImageThumbnailField, VideoThumbnailField
```

----
# simple Model examples to test the fields
###### at first make sure that you made all the setup above
- #### create the models:
in any app inside `models.py` file we will made these two models:

```python 
from django.db import models
from thumb import ImageThumbnailField, VideoThumbnailField

class Media(models.Model):
    video = models.FileField()
    # our Thumbnail
    thumbnail = VideoThumbnailField() # should be VideoThumbnailField(video_field_name="video") but "video" is the default


class MediaTwo(models.Model):
    thumbnail = ImageThumbnailField()
```
- #### now run the migrations in your terminal:

```shell
python manage.py makemigrations
python manage.py migrate
```

- #### add the models to your `admin.py` inside the same app  to test it 

```python 
from django.contrib import admin
from .models import Media, MediaTwo

admin.site.register(Media)
admin.site.register(MediaTwo)
```
---
#### now eveything is ready to test let's test make sure you got the same templates as the pictures below
- ##### in the Model `media` we can choose cascade like `human appear` to caputre at **or** enter the `time MM:SS` **or** just choose random

![media_model](http://a.up-00.com/2018/06/152973557971411.jpeg)

- ##### in the Model `media two` it's just one field `thumbnail` it's normal ImageField but you can add text to it

![media_two_model](http://a.up-00.com/2018/06/152973557990662.jpeg)

---
#### ADD more Cascade choices
- you can add more cascade choices by adding yours in a folder in the your django project dir then add the xml cascade files their, after you've to add the choices in the `settings.py` :
```python
CASCADE_DATA = (
    ('eyes', [os.path.join(BASE_DIR, "<your_cascades_folder>/haarcascade_eyes.xml")]),
    ('human with clear eyes', [os.path.join(BASE_DIR, "<your_cascades_folder>/haarcascade_frontalface.xml"),
                              os.path.join(BASE_DIR, "<your_cascades_folder>/haarcascade_eyes.xml")]),
)

```
- ###### note: you can add more than 1 cascade in the same choice but the each one has to be inside the later like the eyes inside the face ..etc, but don't do it except you really need to because it'll slow down the save process
 
--- 
#### change the cascade accurasy 
- by default each cascade has to be at least **0.3** of the hole width and height of the video frame, you can change it by add in the `settings.py`:
```python
CASCADE_RATIO = {
		"width": <your_value_has_to_be_from_0_to_1>,
                 "height": <your_value_has_to_be_from_0_to_1>,
		 }

```
- ###### note: if you've a choice with multi cascade like **human with smile** each cascade has to have this ratio to the later
---
#### in this project I used:
- opencv in image processing and text writing 
- [jscolor](http://jscolor.com/) in the color field 

