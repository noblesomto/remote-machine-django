from django.db import models
from datetime import datetime
from django import forms
from user.models import Machine, User

# Create your models here.



class Chat(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    req_id = models.CharField(max_length=20, default='0102')
    message = models.TextField(default='Description Message')
    chat_date = models.DateTimeField(default=datetime.now, blank=True)

    @property
    def chatday(self):
        """return the day of the chat"""

        return self.chat_date.strftime('%a %-d %b %Y')

    @property
    def chatime(self):
        """return the time of the chat"""

        return self.chat_date.strftime('%-I:%M%p')

    class Meta:
        db_table = 'chat'

class Serviceman_chat(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    req_id = models.CharField(max_length=20, default='0102')
    message = models.TextField(default='Description Message')
    chat_date = models.DateTimeField(default=datetime.now, blank=True)

    @property
    def chatday(self):
        """return the day of the chat"""

        return self.chat_date.strftime('%a %-d %b %Y')

    @property
    def chatime(self):
        """return the time of the chat"""

        return self.chat_date.strftime('%-I:%M%p')

    class Meta:
        db_table = 'serviceman_chat'
