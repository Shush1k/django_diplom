from django import forms
from django.core.validators import validate_email
from .models import Contact


class ContactForm(forms.ModelForm):
    topic = forms.CharField(max_length=100, required=True,
                            widget=forms.TextInput(attrs={
                                'placeholder': '*Заголовок проблемы..',
                                'class': 'form-control'
                            }))
    email = forms.EmailField(max_length=254, required = False,
                             widget=forms.TextInput(attrs={
                                 'placeholder': '*Email..',
                                 'class': 'form-control'
                             }))
    message = forms.CharField(max_length=1000, required=True,
                              widget=forms.Textarea(attrs={
                                  'placeholder': '*Сообщение..',
                                  'class': 'form-control',
                                  'rows': 6,
                              }))

    class Meta:
        model = Contact
        fields = ('topic', 'email', 'message',)
