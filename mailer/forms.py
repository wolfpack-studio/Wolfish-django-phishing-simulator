from email import message
from django import forms

class MailForm(forms.Form):
    CHOICES = (
        ('text/plain', 'text'),
        ('text/html', 'html')
    )
    sender_email    = forms.EmailField(required=True, widget=forms.TextInput(attrs={"placeholder":"Sender Email","class":"form-control", 'style':'display:block; margin-bottom:4px'}))
    sender_name     = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Sender Name","class":"form-control",'style':'display:block; margin-bottom:15px'}))
    reply_to_email  = forms.EmailField(required=False, widget=forms.TextInput(attrs={"placeholder":"Reply-To Email","class":"form-control", 'style':'display:block; margin-bottom:4px'}))
    reply_to_name   = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder":"Reply-To Name","class":"form-control",'style':'display:block; margin-bottom:15px'}))
    subject         = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Subject","class":"form-control",'style':'display:block; margin-bottom:4px'}))
    message         = forms.CharField(required=True, widget=forms.Textarea(attrs={"id":"editor", "name":"ck", "placeholder":"Message","class":"form-control",'style':'display:block; margin-bottom:4px'}))
    email_list      = forms.CharField(required=True, widget=forms.Textarea(attrs={"placeholder":"Email List","class":"form-control",'style':'display:block; margin-bottom:15px'}))
    #type_selector   = forms.ChoiceField(required=True, choices=CHOICES,  widget=forms.RadioSelect(attrs={ 'style':'display:inline-block; margin-bottom:2px'}))


class AddSenderForm(forms.Form):
    sender_name            = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Nickname","class":"form-control",'style':'display:block; margin-bottom:20px'}))
    sender_email           = forms.EmailField(required=True, widget=forms.TextInput(attrs={"placeholder":"From Email","class":"form-control",'style':'display:block; margin-bottom:4px'}))
    
