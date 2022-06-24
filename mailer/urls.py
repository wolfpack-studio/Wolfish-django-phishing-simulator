from django.urls import path
from .views import *

# app_name = "mailer"

urlpatterns = [
    path('', MailView, name="mail-view"),
    path('add-smtp/', SenderAddView, name="add-sender-view"),
    path('list-mails/', SenderListView, name="list-sender-view"),
    path('detail-mail/<id>/', SenderDetailView, name="detail-sender"),
]