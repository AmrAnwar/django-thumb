from django import forms

from .widget import ColoredTextInput


class ColoredTextFieldForm(forms.MultiValueField):

    def __init__(self,  *args, **kwargs):
        self.widget = ColoredTextInput()
        fields = [
            # text
            forms.CharField(required=False),
            forms.CharField(required=False),
            forms.CharField(required=False),
            forms.TypedChoiceField(required=False),
        ]
        super(ColoredTextFieldForm, self).__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list
