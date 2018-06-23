from django import forms


# TODO VALIDATE VALUE
class ColorFieldWidget(forms.TextInput):
    def __init__(self, attrs=None):
        super(ColorFieldWidget, self).__init__(attrs=attrs)
        self.text_input_template_name = str(self.template_name)
        self.template_name = "colorfield.html"

    class Media:
        js = ['colorfield/colorfield.min.js']

    def get_context(self, name, value, attrs):
        context = super(ColorFieldWidget, self).get_context(name, value, attrs)
        context['widget']['text_input_template_name'] = self.text_input_template_name
        return context
