import os

from django.conf import settings

dir_name = os.path.dirname(__file__)

face_cascade_path = os.path.join(dir_name,
                                 "xml_cascades",
                                 "haarcascade_frontalface_default.xml")
smile_cascade = os.path.join(dir_name,
                             "xml_cascades",
                             "haarcascade_smile.xml")

CASCADE_DATA = (
    ('human appear', [face_cascade_path]),
    ('human with smile', [face_cascade_path, smile_cascade])
)
CASCADE_RATIO = {"width": .3, "height": .3}

try:
    if settings.CASCADE_DATA:
        CASCADE_DATA = CASCADE_DATA + settings.CASCADE_DATA
except AttributeError:
    pass

try:
    if settings.CASCADE_RATIO:
        CASCADE_RATIO = settings.CASCADE_RATIO
except AttributeError:
    pass
