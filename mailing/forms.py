from django import forms

from mailing.models import Messages


class MessageCreateForm(forms.ModelForm):
    """Form  for create message for client"""

    class Meta:
        model = Messages
        fields = ["topic", "body"]
