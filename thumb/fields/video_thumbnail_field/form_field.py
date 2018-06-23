from django import forms
from django.core.validators import RegexValidator

from .widget import VideoThumbnailInput
from ..cascade_data import CASCADE_DATA
from ..django_thumbnail import VideoThumbnail
from ..image_thumnail_field import ImageThumbnailFieldForm
from ..colored_text_field import ColoredTextFieldForm


class VideoThumbnailFieldForm(ImageThumbnailFieldForm):

    def __init__(self, video_capture_help_text=None, text_input_help_text=None, *args, **kwargs):
        video_field_name = kwargs.pop("video_field_name", None)
        self.widget = VideoThumbnailInput(video_field_name, video_capture_help_text, text_input_help_text)
        fields = [
            # hidden fields
            forms.CharField(required=False),
            forms.CharField(required=False),
            forms.TypedChoiceField(required=False),
            forms.CharField(validators=[RegexValidator('^(\d){1,2}\:(\d){1,2}$',
                                        message="please enter the time in this format: MM:SS")],
                            max_length=5, required=False),
            forms.BooleanField(required=False),
            # manual input
            forms.ImageField(required=False),
            # text
            ColoredTextFieldForm(required=False),
        ]
        super(VideoThumbnailFieldForm, self).__init__(child_fields=fields, *args, **kwargs)

    def clean(self, value):
        """
        - value format:
            {
            "data": [
                <str: image path if any>,
                <str: video path if any>,
                <str:cascade choose>,
                <str:specific time ex:MM:SS>,
                <bool:random time>,
                <InMemoryFile: manually submitted Imaged>,
                <list: [<str: font text>,<tuple: text color>, <tuple: text border color>, <str: font style>]>,
            ],
            "is_required": self.is_required,
            "video": submitted_video,
            "submitted_image": submitted_image
            }
        """
        field_data = value['data']
        video = value.get('video')
        font_text = field_data[-1][0]
        font_color = field_data[-1][1:3]
        font_style = field_data[-1][3]
        if video and any(field_data[2:5]):
            capture = VideoThumbnail(file=video,
                                     font_text=font_text,
                                     font_color=font_color,
                                     font_style=font_style)
            cascade_case = field_data[2]
            time = field_data[3]
            random = field_data[4]
            if cascade_case:
                image = capture.capture_by_cascade(CASCADE_DATA[int(cascade_case)][1])
                if image:
                    return image
            # specific time
            if time:
                return capture.capture_by_time(str_time=time)
            # random time
            if random:
                return capture.capture_random()
            # raise error after try all cases
            else:
                if cascade_case:
                    raise forms.ValidationError("error: can't find this cascade in the video")
        return super(VideoThumbnailFieldForm, self).clean(value)
