from django.db import models

# Create your models here.


class Mails(models.Model):
    sender_email    = models.CharField(max_length=255, blank=True, null=True)
    sender_name     = models.CharField(max_length=255, blank=True, null=True)
    reply_to_email  = models.CharField(max_length=255, blank=True, null=True)
    reply_to_name   = models.CharField(max_length=255, blank=True, null=True)
    subject         = models.CharField(max_length=255, blank=True, null=True)
    message         = models.TextField(blank=True, null=True)
    email_list      = models.TextField(blank=True, null=True)
    dt_stamp        = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.id