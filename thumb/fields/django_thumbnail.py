import os
import re
import cv2
import numpy as np


from PIL import Image
from io import BytesIO
from random import randint

from django import forms
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from .cascade_data import CASCADE_RATIO


def convert_rgb_hex_to_bgr_decimal(rgb_hex):
    """
    get str of hex RGB color code and return list of BGR color code
    :param rgb_hex: ex: FFBC89
    :return: tuple of numbers ex: (123, 243, 234)
    """
    bgr_hex_list = re.findall('.{1,2}', rgb_hex)[:3][::-1]
    return tuple(map(lambda color_value: int(color_value, 16), bgr_hex_list))


def convert_from_min_str_to_sec(min_str):
    """
    :param min_str: '1:41'
    :return:  101
    """
    if ":" in min_str:
        m, s = min_str.split(":")
        return int(m[:2]) * 60 + int(s[:2])
    else:
        raise forms.ValidationError("please enter the time in this format: MM:SS")


def convert_image_bgr_to_rgb(cv2_bgr_frame):
    try:
        cv2_image = cv2.cvtColor(cv2_bgr_frame, cv2.COLOR_BGR2RGB)
        return cv2_image
    except cv2.error:
        # error timing for example or whatever
        raise forms.ValidationError("an error happened, please"
                                    " make sure that you entered time available in your video  "
                                    ", and the video works correctly")


class Thumbnail(object):

    def __init__(self, file=None, font_text=None, font_color=None, font_style=None):
        self.file = file
        self.file_name = None
        self.file_path = None
        self.file_format = None
        self.font_text = font_text
        self.font_color = font_color  # list of 2 rgb color strings, ex: ["I'm" , "Alone"]
        self.font_style = int(font_style)

    def convert_from_cv_to_pil_image(self, cv_image, image_format='JPEG'):
        """
        convert from open cv numpy_array to PIL image
        """
        pil_image = Image.fromarray(cv_image)
        thumb_io = BytesIO()
        pil_image.save(thumb_io, format=image_format)
        if self.file_format:
            name = self.file_name
        else:
            name = "%s.jpeg" % self.file_name
        return ContentFile(thumb_io.getvalue(), name=name)

    def generate_image(self, frame):
        if self.font_text:
            frame = self.add_text(frame)
        rgb_frame = convert_image_bgr_to_rgb(frame)
        return self.convert_from_cv_to_pil_image(rgb_frame)

    def add_text(self, frame):
        height, width = frame.shape[:2]
        text_len = len(self.font_text)
        absolute_text_size_unit_per_width = 150
        size_reducer = text_len * text_len
        min_size = 1
        size = max(width / (absolute_text_size_unit_per_width + size_reducer), min_size)
        min_text_width = text_len * size * 8.7
        # absolute position
        text_absolute_width = .5
        text_absolute_length = .8
        # the dynamic position according to len(text) and image size
        text_length_p = int(height * text_absolute_length)
        text_width_p = int(width * text_absolute_width - min_text_width)
        # thick
        thick_unit_per_width = 150
        text_thick = int(round(width / thick_unit_per_width))
        border_thick_ratio_to_text = 4
        border_thick = text_thick * border_thick_ratio_to_text

        if self.font_color[0] != self.font_color[1]:
            # border color
            cv2.putText(frame,
                        self.font_text,
                        (text_width_p, text_length_p),
                        self.font_style, size,
                        convert_rgb_hex_to_bgr_decimal(self.font_color[1]),
                        border_thick)
        # text color
        cv2.putText(frame,
                    self.font_text,
                    (text_width_p, text_length_p),
                    self.font_style, size,
                    convert_rgb_hex_to_bgr_decimal(self.font_color[0]),
                    text_thick)
        return frame


class ImageThumbnail(Thumbnail):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.file, UploadedFile):
            self.file_name = self.file.name
            stream = self.file.open()
            image = Image.open(stream)
            self.cv2_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            stream.close()

        elif isinstance(self.file, str):
            self.file_path = self.file
            self.file_name = os.path.split(self.file)[1]
            # get Image
            self.cv2_img = cv2.imread(self.file_path, cv2.IMREAD_COLOR)
        else:
            raise TypeError("Image has to be the str path or UploadedFile only.")
        self.file_format = os.path.splitext(self.file_name)[1]

    def get_with_text(self):
        return self.generate_image(frame=self.cv2_img)


class VideoThumbnail(Thumbnail):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # TODO NEED TO BE MORE CLEAN
        if isinstance(self.file, UploadedFile):
            try:
                self.file_name = self.file.name.split()[0]
                self.file_path = self.file.file.name
            except AttributeError:
                self.file_path = self.file
                self.file_name = self.file
        elif isinstance(self.file, str):
            self.file_path = self.file
            self.file_name = os.path.split(self.file)[1]
        else:
            raise TypeError("video parameter has to be the str path or UploadedFile only.")
        self.vidcap = None
        try:
            self.vidcap = cv2.VideoCapture(self.file_path)
        except TypeError as ex:
            raise forms.ValidationError("%s: please add a valid video format"
                                        % (type(ex).__name__,))
        # if null video field, or no Temporary file for the video
        except AttributeError:
            if self.file:
                path = default_storage.save('thumbnail_stage/' + str(self.file.name),
                                            ContentFile(self.file.file.read()))
                tmp_file_path = os.path.join(settings.MEDIA_ROOT, path)
                self.vidcap = cv2.VideoCapture(tmp_file_path)
            else:
                raise forms.ValidationError("you have to  add a video with a valid video format")
        self.frames = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.vidcap.get(cv2.CAP_PROP_FPS)
        # get vidcap property
        self.width = int(self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
        self.height = int(self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float

    def capture_random(self):
        random_time = randint(2, int(self.frames / self.fps))
        return self.capture_by_time(time_secs=random_time)

    def capture_by_time(self, str_time=None, time_secs=None):
        """
        :param str_time: in format "MM<number>:SS<number>" or "M:S" or just S<number>
        :param time_secs: integer
        :return: PIL Image
        """
        # if MM:SS format will convert it secs
        if str_time:
            _thumbnail_at = convert_from_min_str_to_sec(str_time)
        elif time_secs:
            _thumbnail_at = time_secs
        else:
            raise ValueError("you have to add the time")
        self.vidcap.set(cv2.CAP_PROP_POS_MSEC, _thumbnail_at * 1000)
        success, cv2_image = self.vidcap.read()
        if not success:
            raise forms.ValidationError(" make sure that you entered time available in your video  "
                                        ", and the video works correctly")
        return self.generate_image(cv2_image)

    def capture_by_cascade(self, cascade_path_list):
        """
        :return: Image or None
        """
        cascade_data_list = [cv2.CascadeClassifier(cascade_path)
                             for cascade_path in cascade_path_list]
        video_length = int(self.frames) - 1
        if self.vidcap.isOpened() and video_length > 0:
            success, frame = self.vidcap.read()
            while success:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if self.check_frame_by_cascade_data(gray_frame, cascade_data_list):
                    return self.generate_image(frame)
                success, frame = self.vidcap.read()
        return None

    def check_frame_by_cascade_data(self, gray_frame, cascade_data_list):
        """
        it's recursive function to handle multi cascade list
        """
        height, width = gray_frame.shape[:2]
        cas_h, cas_w = (int(round(height * CASCADE_RATIO['height'])),
                        int(round(width * CASCADE_RATIO['width'])))
        for cascade in cascade_data_list:
            results = cascade.detectMultiScale(gray_frame,
                                               scaleFactor=1.01,
                                               minNeighbors=5,
                                               minSize=(cas_h, cas_w),
                                               flags=cv2.CASCADE_SCALE_IMAGE)
            try:
                if results.any():
                    for (x, y, w, h) in results:
                        roi_gray = gray_frame[y:y + h, x:x + w]
                        return self.check_frame_by_cascade_data(roi_gray, cascade_data_list[1:])
                else:
                    return False
            except AttributeError:
                return False
        return True
