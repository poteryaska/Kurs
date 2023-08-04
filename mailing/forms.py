from django import forms

from mailing.models import Messages, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class MessageCreateForm(StyleFormMixin, forms.ModelForm):
    """Form  for create message for client"""

    class Meta:
        model = Messages
        fields = ["topic", "body"]


class ClientCreateForm(StyleFormMixin, forms.ModelForm):
    """Form for create client"""

    class Meta:
        model = Client
        fields = ["full_name", "email", "description"]