from django import forms
from django.forms import ModelForm
from django.forms.fields import BooleanField

from main.models import Sending, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class SendingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Sending
        exclude = ('sent_at', 'status', 'owner',)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)

    def clean_theme(self):
        clean_data = self.cleaned_data.get('theme')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

        if clean_data.lower() in forbidden_words:
            raise forms.ValidationError('Недопустимое слово в теме письма')
        return clean_data

    def clean_text(self):
        clean_data = self.cleaned_data.get('text')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        if clean_data.lower() in forbidden_words:
            raise forms.ValidationError('Недопустимое слово в тексте письма')
        return clean_data


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)


class SendingModerationForm(SendingForm):
    class Meta:
        model = Sending
        fields = ('is_active',)
