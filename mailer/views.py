from django.shortcuts import render
from .forms import MailForm, AddSMTP
# sendinblue imports
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage, send_mass_mail
from .models import Mails, Backend
from django.core.mail.backends.smtp import EmailBackend
import django.conf as conf
from django.template import Template


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



                b = Backend.objects.all()[0]
                backend = EmailBackend(host=b.email_host, port=b.email_port, username=b.email_host_user, 
                                    password=b.email_host_password, use_tls=b.email_use_tls, fail_silently=True)

                emails = email_list.splitlines()
                emails = [i.strip() for i in emails]


                # Reply-to validation
                if reply_to_email == "":
                    
                    for i in emails:
                        msg = EmailMultiAlternatives(
                                    subject,
                                    message,
                                    from_email=sender_name+ '<'+sender_email+'>',
                                    to=[i],
                                    connection=backend,
                                    )
                        msg.attach_alternative(message, "text/html")
                        msg.send()
                    Mails.objects.create(sender_email=sender_email,sender_name=sender_name,
                                                subject=subject, message=message, email_list=email_list)
                else:
                    for i in emails:
                        msg = EmailMultiAlternatives(
                                    subject,
                                    message,
                                    from_email=sender_name+ '<'+sender_email+'>',
                                    to=[i],
                                    reply_to=[reply_to_name+ '<'+reply_to_email+'>'],
                                    connection=backend,
                                    )
                        msg.attach_alternative(message, "text/html")
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

                EMAIL_HOST = email_host.strip()
                EMAIL_HOST_USER = email_host_user.strip()
                EMAIL_HOST_PASSWORD = email_host_password.strip()
                EMAIL_PORT = int(email_port)

                bl = True
                if email_use_tls == 'true':
                    bl = True
                if email_use_tls == 'false':
                    bl = False

                Backend.objects.all().delete()
                Backend.objects.create(email_host=EMAIL_HOST, email_host_user=EMAIL_HOST_USER,
                                        email_host_password=EMAIL_HOST_PASSWORD, email_port=EMAIL_PORT,
                                        email_use_tls=bl)


                return render(request, 'response.html', {"response": "SMTP added successfuly"})

                

            except Exception as e:
                return render(request, 'response.html', {"response": e})

        else:
            return render(request, 'response.html', {"response": "Incorrect input format"})

    else:
        backend = Backend.objects.all()
        data = {}
        if len(backend) > 0:
            backend = backend[0]
            data = {'EMAIL_HOST': backend.email_host, 'EMAIL_HOST_USER': backend.email_host_user, 
                    'EMAIL_HOST_PASSWORD': backend.email_host_password, 'EMAIL_PORT': backend.email_port,
                    'EMAIL_USE_TLS': backend.email_use_tls}
        else:
            data = {'EMAIL_HOST': None, 'EMAIL_HOST_USER': None, 
                    'EMAIL_HOST_PASSWORD': None, 'EMAIL_PORT': None,
                    'EMAIL_USE_TLS': None}
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
        