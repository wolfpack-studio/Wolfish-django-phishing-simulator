from importlib import import_module
from django.shortcuts import render
from .forms import MailForm, AddSMTP
# sendinblue imports
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage, send_mass_mail
from .models import MailTemplate, Mails, Backend, PhishingData, PhishingDataDict, PhishingLink, Recipient
from django.core.mail.backends.smtp import EmailBackend
import django.conf as conf
from django.template import Template
from django.http import HttpResponse
from phishing.settings import BACKEND_URL

def get_links(s, first, last):
    start_sep=first
    end_sep=last
    result=[]
    tmp=s.split(start_sep)
    for par in tmp:
        if end_sep in par:
            result.append(par.split(end_sep)[0])
    return result




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

                valid_message = message.replace("&lt;phish&gt;","")
                valid_message = valid_message.replace("&lt;/phish&gt;","")

                b = Backend.objects.all()[0]

                backend = EmailBackend(host=b.email_host, port=b.email_port, username=b.email_host_user, 
                                    password=b.email_host_password, use_tls=b.email_use_tls, fail_silently=True)

                # backend = EmailBackend(host="smtpout.secureserver.net" , port="465", username="Syed@quadrimetanoia.com", 
                #                     password="2Xgh2%/BJ8?EUQ8", use_tls=True, fail_silently=True)
                

                emails = email_list.splitlines()
                emails = [i.strip() for i in emails]

                m = Mails.objects.create(sender_email=sender_email,sender_name=sender_name,
                                                subject=subject, message=valid_message, email_list=email_list)

                # Enter data in links
                links = get_links(message, "&lt;phish&gt;", "&lt;/phish&gt;")
                for i in links:
                    PhishingLink.objects.create(link = i, mail=m)

                # Reply-to validation
                if reply_to_email == "":
                    
                    for i in emails:
                        mail_body = valid_message

                        if "@" and "." in i:
                            r = Recipient.objects.create(email=i, mail=m)
                        else:
                            r = Recipient.objects.create(email=i, mail=m, valid=False)
                        for j in links:
                            mail_body = mail_body.replace(j, j+"/"+m.unq_id+"-"+r.unq_id)
                        
                        msg = EmailMessage(
                                    subject,
                                    mail_body,
                                    from_email=sender_name+ '<'+sender_email+'>',
                                    to=[i],
                                    connection=backend,
                                    )
                        msg.content_subtype = "html"
                        msg.send()
                        
                    
                                                
                else:
                    for i in emails:
                        mail_body = valid_message
                        if "@" and "." in i:
                            r = Recipient.objects.create(email=i, mail=m)
                        else:
                            r = Recipient.objects.create(email=i, mail=m, valid=False)
                        for j in links:
                            mail_body = mail_body.replace(j, j+"/"+m.unq_id+"-"+r.unq_id)
                        msg = EmailMessage(
                                    subject,
                                    mail_body,
                                    from_email=sender_name+ '<'+sender_email+'>',
                                    to=[i],
                                    reply_to=[reply_to_name+ '<'+reply_to_email+'>'],
                                    connection=backend,
                                    )
                        msg.content_subtype = "html"
                        msg.send()
                        
                    

                    # Enter data in links
                    links = get_links(message, "&lt;phish&gt;", "&lt;/phish&gt;")
                    for i in links:
                        PhishingLink.objects.create(link = i, mail=m)


                return render(request, 'response.html', {"response": "Email sent successfully"})
            
            except Exception as e:
                return render(request, 'response.html', {"response": e})

        else:
            return render(request, 'response.html', {"response": "Incorrect input format"})
        
    else:
        form = MailForm()
        temps = MailTemplate.objects.all()
        return render(request, 'mail.html', {'form':form, 'temps':temps, 'b_url':BACKEND_URL})


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
        if data.email_list == None:
            res = []
        else:
            emails = data.email_list.splitlines()
            res = [i.strip() for i in emails]
            act_res = Recipient.objects.filter(mail__id=data.id)
        return render(request, 'detail_mail.html', {"data":data, "res":res, "act_res":act_res})
        

def UserDetailView(request, mail_unq_id, user_unq_id):
    if request.method == 'GET':
        data=[]
        links = PhishingLink.objects.filter(mail__unq_id=mail_unq_id)
        for i in links:
            pdata = []
            click_count = 0
            d = PhishingData.objects.filter(link__id=i.id, recipient__unq_id=user_unq_id)
            if len(d) > 0:
                click_count = d[0].click_count
            if len(d) > 0:
                p = PhishingDataDict.objects.filter(pdata__id=d[0].id)
                for j in p:
                    pdata.append(eval(j.data))
    
            data.append({"link":i.link, "click_count":click_count, "pdata":pdata})
        print(data)

        return render(request, 'detail_user.html', {"data":data})


def RenderTemplate(request):
    demo = """<!DOCTYPE html>
                <html>
                <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                body {
                padding: 25px;
                background-color: white;
                color: black;
                font-size: 25px;
                }

                .dark-mode {
                background-color: black;
                color: white;
                }
                </style>
                </head>
                <body>

                <input type="text" name="name">
                <input type="submit" name="submit" value="Update SMTP">

                <h2>Toggle Dark/Light Mode</h2>
                <p>Click the button to toggle between dark and light mode for this page.</p>

                <button onclick="myFunction()">Toggle dark mode</button>

                <script>
                function myFunction() {
                var element = document.body;
                element.classList.toggle("dark-mode");
                }
                </script>

                </body>
                </html>


                """
    return HttpResponse(demo)



def DynamicTemplate(request, url_slug, render_id):
    try:
        temp_instance = MailTemplate.objects.get(url_slug=url_slug)
        mail_id, rpt_id = render_id.split("-")
        l = None
        links = PhishingLink.objects.filter(mail__unq_id=mail_id)
        for link in links:
            if url_slug in link.link:
                l=link
    except MailTemplate.DoesNotExist:
        return HttpResponse("Template does not exist")

    if request.method == 'GET':
        if l:    
            p_data = PhishingData.objects.filter(link__id=l.id, recipient__unq_id=rpt_id)
            if len(p_data) > 0:
                p_data = p_data[0]
                p_data.click_count = p_data.click_count + 1
                p_data.save()
            else:
                r = Recipient.objects.get(unq_id=rpt_id)
                PhishingData.objects.create(link=l, recipient=r, click_count=1)
        return HttpResponse(temp_instance.template_code)

    if request.method == 'POST':
        print(str(request.POST.dict()))
        if l:    
            p_data = PhishingData.objects.filter(link__id=l.id, recipient__unq_id=rpt_id)
            if len(p_data) > 0:
                p_data = p_data[0]
                PhishingDataDict.objects.create(pdata=p_data, data=str(request.POST.dict()))
        return HttpResponse(temp_instance.template_code)
        