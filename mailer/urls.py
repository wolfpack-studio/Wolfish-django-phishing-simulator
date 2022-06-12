from django.urls import path
from .views import *

urlpatterns = [
    path('', MailView, name="mail-view"),
    path('add-sender/', SenderAddView, name="add-sender-view"),
]