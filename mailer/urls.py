from django.urls import path
from .views import *

# app_name = "mailer"

urlpatterns = [
    path('', MailView, name="mail-view"),
    path('login/', Login, name="login"),
    path('logout/', logout_view, name="logout"),
    path('add-smtp/', SenderAddView, name="add-sender-view"),
    path('list-mails/', SenderListView, name="list-sender-view"),
    path('detail-mail/<id>/', SenderDetailView, name="detail-sender"),
    path('user-data/<mail_unq_id>/<user_unq_id>/', UserDetailView, name="user-detail"),
    path('temp/', RenderTemplate, name="render-template"),
    path('render-template/<url_slug>/<render_id>', DynamicTemplate, name="dyn-template"),
]