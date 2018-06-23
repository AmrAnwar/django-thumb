from django import forms

from .widget import ImageThumbnailInput
from ..django_thumbnail import ImageThumbnail
from ..colored_text_field import ColoredTextFieldForm


class ImageThumbnailFieldForm(forms.MultiValueField):
    widget = ImageThumbnailInput()

    def __init__(self, child_fields=None,  *args, **kwargs):
        fields = child_fields or [
            # hidden fields to get pre submitted image
            forms.CharField(required=False),
            forms.ImageField(required=False),
            # text
            ColoredTextFieldForm(required=False),
        ]
        kwargs.pop('max_length')
        kwargs.pop('widget')
        kwargs['require_all_fields'] = False
        super(ImageThumbnailFieldForm, self).__init__(fields=fields, *args, **kwargs)

    def clean(self, value):
        """
        - value format:
            {
            "data": field_data<<[
                <str: image path if any>
                <InMemoryFile: image>
                <list: colored text [<str: font text>,
                                    <str: text color>,
                                    <str: text border color>,
                                    <str: font style>],
                                    ],
            "is_required": self.is_required,
            "submitted_image": submitted_image
            }
        - value example:
            {
            }
        """
        field_data = value['data']
        image = value.get('submitted_image')
        font_text = field_data[-1][0]
        font_color = field_data[-1][1:3]
        font_style = field_data[-1][3]
        if image and font_text:
            img_thumbnail = ImageThumbnail(file=image,
                                           font_text=font_text,
                                           font_color=font_color,
                                           font_style=font_style)
            return img_thumbnail.get_with_text()
        return field_data[-2]  # return super(ImageThumbnailFieldForm, self).clean(field_data[-5])

    def compress(self, data_list):
        return data_list
