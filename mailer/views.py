from django.shortcuts import render
from .forms import MailForm, AddSenderForm
from django.http import HttpResponse
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from phishing.settings import SENDGRID_API_KEY
from sendgrid import SendGridAPIClient
import json


def MailView(request):
    if request.method == "POST":
        form = MailForm(request.POST)
        if form.is_valid():
            try:
                sender_email    = form.cleaned_data['sender_email']
                sender_name     = form.cleaned_data['sender_name']
                subject         = form.cleaned_data['subject']
                message         = form.cleaned_data['message']
                email_list      = form.cleaned_data['email_list']
                #type_selector   = form.cleaned_data['type_selector']
                


                sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

                from_email = Email(sender_email.strip(), sender_name)
                subject = subject

                emails = email_list.split(",")
                emails = [(a.strip(), "") for a in emails]
                
                to_email = emails
                content = Content("text/html", message)
                
                mail = Mail(from_email, to_email, subject, content, is_multiple=True)

                # Get a JSON-ready representation of the Mail object
                mail_json = mail.get()

                # Send an HTTP POST request to /mail/send
                response = sg.client.mail.send.post(request_body=mail_json)
                print(response.status_code)
                print(response.headers)

                return render(request, 'response.html', {"response": "Email sent successfully"})
            
            except Exception as e:
                return render(request, 'response.html', {"response": e})
    else:
        form = MailForm()
        return render(request, 'mail.html', {'form':form})



def SenderAddView(request):
    
    if request.method == "POST":
        form = AddSenderForm(request.POST)
        if form.is_valid():
            try:
                nickname        = form.cleaned_data['nickname']
                from_email      = form.cleaned_data['from_email']
                from_name       = form.cleaned_data['from_name']
                reply_to_email  = form.cleaned_data['reply_to_email']
                reply_to_name   = form.cleaned_data['reply_to_name']
        
                sg = SendGridAPIClient(SENDGRID_API_KEY)

                data = {
                    "nickname": nickname,
                    "from_email": from_email.strip(),
                    "from_name": from_name,
                    "reply_to": reply_to_email.strip(),
                    "reply_to_name": reply_to_name,
                    "address": "1234 Fake St",
                    "address2": "PO Box 1234",
                    "state": "CA",
                    "city": "San Francisco",
                    "country": "USA",
                    "zip": "94105"
                }

                response = sg.client.verified_senders.post(
                    request_body=data
                )
                print(response.status_code)
                print(response.body)
                print(response.headers)

                return render(request, 'response.html', {"response": "Verification email sent successfuly. Check Inbox"})

            except Exception as e:
                return render(request, 'response.html', {"response": e})


    else:
        form = AddSenderForm()
        return render(request, 'add-sender.html', {'form':form})





def SenderListView(request):

    if request.method == "POST":
        print(dict(request.POST))
        sg = SendGridAPIClient(SENDGRID_API_KEY)

        for id in dict(request.POST)["ids"]:
            response = sg.client.verified_senders._(id).delete()
        return render(request, 'response.html', {"response": "Operation is performed."})
    

    else:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.client.verified_senders.get()

        print(response.status_code)
        print(response.body.decode("utf-8"))
        print(response.headers)
        data = json.loads(response.body.decode("utf-8"))["results"]


        return render(request, 'list-senders.html', {"data":data})