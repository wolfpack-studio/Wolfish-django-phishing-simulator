from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Mails, MailTemplate, Recipient, PhishingData, PhishingLink, PhishingDataDict])