from django.contrib import admin
from .models import Mails, MailTemplate
# Register your models here.
admin.site.register([Mails, MailTemplate])