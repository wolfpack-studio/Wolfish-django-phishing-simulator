from django.shortcuts import render
from .forms import MailForm, AddSMTP
# sendinblue imports
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Mails
import pytz

import django.conf as conf



# View to send emails
def MailView(request):
    if request.method == "POST":        

        # Fetching data from form
        form = MailForm(request.POST)
        if form.is_valid():
            try:
                sender_email    = form.cleaned_data['sender_email']
                sender_name     = form.cleaned_data['sender_name']
                reply_to_email    = form.cleaned_data['reply_to_email']
                reply_to_name     = form.cleaned_data['reply_to_name']
                subject         = form.cleaned_data['subject']
                message         = form.cleaned_data['message']
                email_list      = form.cleaned_data['email_list']
                #type_selector   = form.cleaned_data['type_selector']

                emails = email_list.splitlines()
                emails = [i.strip() for i in emails]

                # Reply-to validation
                if reply_to_email == "":
                    a = send_mail(
                            subject,
                            message,
                            sender_name+ '<'+sender_email+'>',
                            emails,
                            fail_silently=False,
                                )
                    if a == 1:
                        Mails.objects.create(sender_email=sender_email,sender_name=sender_name,
                                                subject=subject, message=message, email_list=email_list)
                else:
                    msg = EmailMultiAlternatives(
                                subject,
                                message,
                                from_email=sender_name+ '<'+sender_email+'>',
                                to=emails,
                                reply_to=[reply_to_name+ '<'+reply_to_email+'>'],
                                
                                )
                    msg.send()
                    Mails.objects.create(sender_email=sender_email,sender_name=sender_name, 
                                                reply_to_email=reply_to_email, reply_to_name=reply_to_name,
                                                subject=subject, message=message, email_list=email_list)
                    #conf.settings.DEBUG = False


                return render(request, 'response.html', {"response": "Email sent successfully"})
            
            except Exception as e:
                return render(request, 'response.html', {"response": e})

        else:
            return render(request, 'response.html', {"response": "Incorrect input format"})
        
    else:
        form = MailForm()
        return render(request, 'mail.html', {'form':form})


# Add sender view
def SenderAddView(request):
    if request.method == "POST":

        # Fetching data from form
        form = AddSMTP(request.POST)
        if form.is_valid():
            try:
                email_host          = form.cleaned_data['email_host']
                email_host_user        = form.cleaned_data['email_host_user']
                email_host_password = form.cleaned_data['email_host_password']
                email_port          = form.cleaned_data['email_port']
                email_use_tls       = form.cleaned_data['email_use_tls']

                conf.settings.EMAIL_HOST = email_host.strip()
                conf.settings.EMAIL_HOST_USER = email_host_user.strip()
                conf.settings.EMAIL_HOST_PASSWORD = email_host_password.strip()
                conf.settings.EMAIL_PORT = int(email_port)

                bl = True
                if email_use_tls == 'true':
                    bl = True
                if email_use_tls == 'false':
                    bl = False
                conf.settings.EMAIL_USE_TLS = bl


                return render(request, 'response.html', {"response": "SMTP added successfuly"})

                

            except Exception as e:
                return render(request, 'response.html', {"response": e})

        else:
            return render(request, 'response.html', {"response": "Incorrect input format"})

    else:
        data = {'EMAIL_HOST': conf.settings.EMAIL_HOST, 'EMAIL_HOST_USER': conf.settings.EMAIL_HOST_USER, 
                'EMAIL_HOST_PASSWORD': conf.settings.EMAIL_HOST_PASSWORD, 'EMAIL_PORT': conf.settings.EMAIL_PORT,
                'EMAIL_USE_TLS': conf.settings.EMAIL_USE_TLS}
        form = AddSMTP()
        return render(request, 'add-sender.html', {'form':form, 'data':data})




# Sender listing view with delete functionality.
def SenderListView(request):

    if request.method == 'GET':
        data = Mails.objects.all()
        return render(request, 'list-senders.html', {"data":data})


def SenderDetailView(request, id):

    if request.method == 'GET':
        data = Mails.objects.get(id=id)
        emails = data.email_list.splitlines()
        res = [i.strip() for i in emails]
        return render(request, 'detail_mail.html', {"data":data, "res":res})
        