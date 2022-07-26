from dataclasses import dataclass
from django.db import models
import random
import string
from django.db.models.signals import pre_save, post_save

# Create your models here.



class Mails(models.Model):
    unq_id          = models.CharField(max_length=255, blank=True, null=True, unique=True)
    sender_email    = models.CharField(max_length=255, blank=True, null=True)
    sender_name     = models.CharField(max_length=255, blank=True, null=True)
    reply_to_email  = models.CharField(max_length=255, blank=True, null=True)
    reply_to_name   = models.CharField(max_length=255, blank=True, null=True)
    subject         = models.CharField(max_length=255, blank=True, null=True)
    message         = models.TextField(blank=True, null=True)
    email_list      = models.TextField(blank=True, null=True)
    dt_stamp        = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Mail"




class Recipient(models.Model):
    unq_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    valid = models.BooleanField(default=True)
    mail  = models.ForeignKey(Mails, on_delete=models.CASCADE, related_name="recipients", blank=True, null=True)
    
    def __str__(self):
        return str(self.id)


class PhishingLink(models.Model):
    link = models.CharField(max_length=255, blank=True, null=True)
    mail  = models.ForeignKey(Mails, on_delete=models.CASCADE, related_name="links", blank=True, null=True)

    def __str__(self):
        return str(self.id)

class PhishingData(models.Model):
    link        = models.ForeignKey(PhishingLink, on_delete=models.CASCADE)
    recipient   = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)
    agent_data  = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class PhishingDataDict(models.Model):
    pdata  = models.ForeignKey(PhishingData, on_delete=models.CASCADE, blank=True, null=True)
    data   = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)



class Backend(models.Model):
    email_host              = models.CharField(max_length=255, blank=True, null=True)
    email_host_user         = models.CharField(max_length=255, blank=True, null=True)
    email_host_password     = models.CharField(max_length=255, blank=True, null=True)
    email_port              = models.CharField(max_length=255, blank=True, null=True)
    email_use_tls           = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class MailTemplate(models.Model):
    template_name               = models.CharField(max_length=255, blank=True, null=True)
    url_slug                    = models.CharField(max_length=255, blank=True, null=True, unique=True)
    template_code               = models.TextField(blank=True, null=True)


    def __str__(self):
        return str(self.id) if self.template_name == "" or None else self.template_name









def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_id_generator(instance):
	new_id= random_string_generator()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(unq_id=new_id).exists()
	if qs_exists:
		return unique_id_generator(instance)
	return new_id



def pre_save_create_id(sender, instance, *args, **kwargs):
    if not instance.unq_id:
        instance.unq_id= unique_id_generator(instance)
pre_save.connect(pre_save_create_id, sender=Recipient)


def pre_save_create_id(sender, instance, *args, **kwargs):
    if not instance.unq_id:
        instance.unq_id= unique_id_generator(instance)
pre_save.connect(pre_save_create_id, sender=Mails)