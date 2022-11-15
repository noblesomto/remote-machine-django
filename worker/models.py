from django.db import models
from datetime import datetime
from django import forms
from user.models import Machine, User

# Create your models here.
class Requests(models.Model):
    req_id = models.CharField(max_length=20, default='010203')
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250, default='subject')
    request_status = models.CharField(max_length=250, default='Pending')
    request_type = models.CharField(max_length=200, default='Maintainance')
    description = models.TextField(default='Description Body')
    req_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table = 'request'

class RequestImage(models.Model):
    req_id = models.CharField(max_length=20, default='0102')
    image = models.ImageField(upload_to="requests/")

    class Meta:
        db_table = 'requestimage'


class Chat(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)
    message = models.TextField(default='Description Message')
    chat_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table = 'chat'