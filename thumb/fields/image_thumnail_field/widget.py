from django import forms
from django.conf import settings

from ..colored_text_field import ColoredTextInput


class ImageThumbnailInput(forms.MultiWidget):

    class Media:
        if settings.DEBUG:
            css = {'all': ('thumbnail-field/thumbnail-field.css',)}
        else:
            css = {'all': ('thumbnail-field/thumbnail-field.min.css',)}

    template_name = 'image_thumbnail.html'

    def __init__(self, child_widgets=None, text_input_help_text=None, attrs=None):
        # for update case
        self.initial_data = None
        self.text_input_help_text = text_input_help_text
        widgets = child_widgets or [
            # to get the Image value
            forms.HiddenInput(attrs=attrs),
            # for manual input
            forms.ClearableFileInput(attrs=attrs),
            # colored text
            ColoredTextInput(attrs=attrs)
        ]

        super(ImageThumbnailInput, self).__init__(widgets=widgets, attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super(ImageThumbnailInput, self).get_context(name, value, attrs)
        context['widget']['text_input_help_text'] = self.text_input_help_text
        if value:
            context['value'] = value
        return context

    def decompress(self, value):
        default_list = [None]
        widgets_count = len(self.widgets)
        if getattr(value, 'instance', None):
            cascade_value_list = widgets_count * default_list
            try:
                cascade_value_list[0] = value.file.name
            except ValueError:
                cascade_value_list[0] = None
            # put value in ClearableFileInput() obj
            cascade_value_list[-2] = value
            return cascade_value_list
        return [None] * widgets_count

    def value_from_datadict(self, data, files, name):
        data = super(ImageThumbnailInput, self).value_from_datadict(data, files, name)
        field_data = list(data)
        submitted_image = field_data[-2] or field_data[0]  # string path to image or InMemoryFile
        new_data_dict = {"data": field_data,
                         "is_required": self.is_required,
                         "submitted_image": submitted_image}
        return new_data_dict
