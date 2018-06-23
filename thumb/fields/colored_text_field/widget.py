from django import forms
from django.conf import settings

from ..colorfield import ColorFieldWidget

FONT_CHOICES = [
    ('0', 'sans-serif'),
    ('1', 'small size sans-serif'),
    ('2', 'duplex sans-serif'),
    ('3', 'serif font'),
    ('4', 'complex serif'),
    ('5', 'small complex serif'),
    ('6', 'hand writing'),
    ('7', 'complex hand writing '),
    ('16', 'italic'),
]


class ColoredTextInput(forms.MultiWidget):

    class Media:
        if settings.DEBUG:
            css = {'all': ('thumbnail-field/thumbnail-field.css',)}
        else:
            css = {'all': ('thumbnail-field/thumbnail-field.min.css',)}

    def __init__(self,  attrs=None):
        self.template_name = "coloredtext_field.html"
        widgets = [
            forms.TextInput(attrs={'label': 'text string', 'placeholder': 'text string'}),
            ColorFieldWidget(attrs={'label': 'text color'}),
            ColorFieldWidget(attrs={'label': 'border color'}),
            forms.Select(attrs={'label': 'font'}, choices=FONT_CHOICES)
        ]

        super(ColoredTextInput, self).__init__(widgets=widgets, attrs=attrs)

    def decompress(self, value):
        if value:
            return value
        return [None, None, None, None]
