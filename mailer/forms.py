from email import message
from django import forms

class MailForm(forms.Form):
    CHOICES = (
        ('text/plain', 'text'),
        ('text/html', 'html')
    )
    sender_email    = forms.EmailField(required=True, widget=forms.TextInput(attrs={'style':'display:block; margin-bottom:4px'}))
    sender_name     = forms.CharField(required=True, widget=forms.TextInput(attrs={'style':'display:block; margin-bottom:15px'}))
    subject         = forms.CharField(required=True, widget=forms.TextInput(attrs={'style':'display:block; margin-bottom:4px'}))
    message         = forms.CharField(required=True, widget=forms.Textarea(attrs={'style':'display:block; margin-bottom:4px'}))
    email_list      = forms.CharField(required=True, widget=forms.Textarea(attrs={'style':'display:block; margin-bottom:15px'}))
    type_selector   = forms.ChoiceField(required=True, choices=CHOICES,  widget=forms.RadioSelect(attrs={'style':'display:inline-block; margin-bottom:2px'}))


class AddSenderForm(forms.Form):
    nickname            = forms.CharField(required=True, widget=forms.TextInput(attrs={'style':'display:block; margin-bottom:20px'}))
    from_email          = forms.EmailField(required=True, widget=forms.TextInput(attrs={'style':'display:block; margin-bottom:4px'}))
    from_name     = forms.CharField(required=True, widget=forms.TextInput(attrs={'style':'display:block; margin-bottom:20px'}))
    reply_to_email      = forms.EmailField(required=True, widget=forms.TextInput(attrs={'style':'display:block; margin-bottom:4px'}))
    reply_to_name       = forms.CharField(required=True, widget=forms.TextInput(attrs={'style':'display:block; margin-bottom:20px'}))
