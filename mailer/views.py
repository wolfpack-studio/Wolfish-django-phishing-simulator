from re import I
from django.shortcuts import render
from .forms import MailForm, AddSenderForm
from django.http import HttpResponse
from phishing.settings import SENDINBLUE_API_KEY
# sendinblue imports
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException



# Api configs 
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = SENDINBLUE_API_KEY



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
                

                emails = email_list.split(",")
                emails = [{"email": a.strip()} for a in emails]

                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

                subject = subject
                html_content = message
                sender = {"name":sender_name,"email":sender_email}
                reply_to = {"email":reply_to_email,"name":reply_to_name}
                to = emails
                headers = {"Some-Custom-Name":"unique-id-1234"}

                # getting sender details
                sender_info = get_sender_info(sender_email)

                # Existing sender validation
                if (sender_info == None) or sender_info["active"] == False:
                     return render(request, 'response.html', {"response": "Sender is not active"})

                # Reply-to validation
                if reply_to_email == "":
                    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)
                else:
                    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)

                # send mail
                api_response = api_instance.send_transac_email(send_smtp_email)
                print(api_response)

                return render(request, 'response.html', {"response": "Email sent successfully"})
            
            except Exception as e:
                return render(request, 'response.html', {"response": e})

        else:
            return render(request, 'response.html', {"response": "Incorrect input format"})
        
    else:
        form = MailForm()
        return render(request, 'mail.html', {'form':form})


# Utility function to get sender info in exists.
def get_sender_info(email):
    api_instance = sib_api_v3_sdk.SendersApi(sib_api_v3_sdk.ApiClient(configuration))
    api_response = api_instance.get_senders()
    data = api_response.to_dict()["senders"]

    sender = None
    for i in data:
        if i["email"] == email:
            sender = {"id":i["id"], "active":i["active"]}
    return sender



# Add sender view
def SenderAddView(request):
    if request.method == "POST":

        # Fetching data from form
        form = AddSenderForm(request.POST)
        if form.is_valid():
            try:
                sender_name        = form.cleaned_data['sender_name']
                sender_email       = form.cleaned_data['sender_email']

                api_instance = sib_api_v3_sdk.SendersApi(sib_api_v3_sdk.ApiClient(configuration))
                
                # Check existing sender
                sender = get_sender_info(sender_email)

                if sender == None:
                    sender = sib_api_v3_sdk.CreateSender(name = sender_name, email=sender_email)
                    api_response = api_instance.create_sender(sender=sender)
                    print(api_response)
                    return render(request, 'response.html', {"response": "Verification email sent successfuly. Check Inbox"})

                else:
                    
                    if sender["active"] == True:
                        return render(request, 'response.html', {"response": "Sender is already active"})
                    else:
                        api_response = api_instance.delete_sender(sender["id"])
                        sender = sib_api_v3_sdk.CreateSender(name = sender_name, email=sender_email)
                        api_response = api_instance.create_sender(sender=sender)
                        return render(request, 'response.html', {"response": "Verification email sent again. Check Inbox"})

            except Exception as e:
                return render(request, 'response.html', {"response": e})

        else:
            return render(request, 'response.html', {"response": "Incorrect input format"})

    else:
        form = AddSenderForm()
        return render(request, 'add-sender.html', {'form':form})




# Sender listing view with delete functionality.
def SenderListView(request):
    # Go for delete if post request
    if request.method == "POST":
        api_instance = sib_api_v3_sdk.SendersApi(sib_api_v3_sdk.ApiClient(configuration))
        # Delete senders
        for id in dict(request.POST)["ids"]:
            api_response = api_instance.delete_sender(id)
        return render(request, 'response.html', {"response": "Operation is performed."})
   
    # Or else list the senders
    else:
        api_instance = sib_api_v3_sdk.SendersApi(sib_api_v3_sdk.ApiClient(configuration))
        api_response = api_instance.get_senders()
        data = api_response.senders
        return render(request, 'list-senders.html', {"data":data})

        