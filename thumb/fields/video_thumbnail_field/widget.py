from django import forms

from ..colored_text_field import ColoredTextInput
from ..cascade_data import CASCADE_DATA
from ..image_thumnail_field import ImageThumbnailInput

CASCADE_CHOICES = list(
    [("", "select a cascade case")] +
    [(str(cascade_index), cascade[0])
     for cascade_index, cascade in enumerate(CASCADE_DATA)]
)


class VideoThumbnailInput(ImageThumbnailInput):

    def __init__(self, video_field_name, video_capture_help_text=None, attrs=None):
        self.video_field_name = video_field_name or "video"
        self.video_capture_help_text = (video_capture_help_text
                                        or "if checked or entered data in more than 1 field, it will execute in order")
        # for update case
        self.video = None
        widgets = [
            # to get the image path
            forms.HiddenInput(attrs=attrs),
            # to get the video value
            forms.HiddenInput(attrs=attrs),
            # capture options
            forms.Select(choices=CASCADE_CHOICES),
            forms.TextInput(attrs={'placeholder': 'MM:SS'}),
            forms.CheckboxInput(attrs={'label': "random", "note": "get random thumbnail"}, ),
            # for manual input
            forms.ClearableFileInput(attrs=attrs),
            # color
            ColoredTextInput(attrs=attrs)
        ]
        super(VideoThumbnailInput, self).__init__(child_widgets=widgets, attrs=attrs)
        self.template_name = "video_thumbnail.html"

    def get_context(self, name, value, attrs):
        context = super(VideoThumbnailInput, self).get_context(name, value, attrs)
        context['widget']['video_capture_help_text'] = self.video_capture_help_text
        return context

    def decompress(self, value):
        image_value = value
        value = super(VideoThumbnailInput, self).decompress(value)
        if any(value):
            video = getattr(image_value.instance, self.video_field_name, None)
            try:
                value[1] = video.path
            except ValueError:
                value[1] = None
        return value

    def value_from_datadict(self, data, files, name):
        value = super(VideoThumbnailInput, self).value_from_datadict(data, files, name)
        submitted_video = files.get(self.video_field_name) or value['data'][1]
        value['video'] = submitted_video
        return value
