from django.db import models
from django.utils import timezone
from datetime import datetime


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=200, default='First Name')
    last_name = models.CharField(max_length=200, default='Last Name')
    user_picture = models.ImageField(upload_to='profile/', null=True)
    phone = models.CharField(max_length=200, default='Phone')
    email = models.CharField(max_length=250, default='email')
    user_category = models.CharField(max_length=250, default='user category')
    password = models.CharField(max_length=200, default='null')
    user_status = models.CharField(max_length=100, default='Account Status')
    reg_date = models.DateTimeField(default=timezone.now, blank=True)


    class Meta:
        db_table = 'user'



class Machine(models.Model):
    machine_name = models.CharField(max_length=200, )
    machine_code = models.CharField(max_length=350, default='')
    machine_worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='m_users')
    machine_expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name='m_experts')
    machine_serviceman = models.ForeignKey(User, on_delete=models.CASCADE, related_name='m_serviceman')
    machine_picture = models.ImageField(upload_to='machine/', null=True)
    machine_type = models.CharField(max_length=100, default='Machine')
    machine_status = models.CharField(max_length=100, default='Status')

    class Meta:
        db_table = 'machine'

class Requests(models.Model):
    req_id = models.CharField(max_length=20, default='010203')
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250, default='subject')
    request_status = models.CharField(max_length=250, default='Pending')
    request_type = models.CharField(max_length=200, default='Assistance')
    description = models.TextField(default='Description Body')
    req_date = models.DateTimeField(default=datetime.now, blank=True)
    worker_status = models.CharField(max_length=250, default='Pending')
    expert_status = models.CharField(max_length=250, default='Pending')
    serviceman_status = models.CharField(max_length=250, default='Pending')
    request_sender = models.CharField(max_length=50, default='Worker')
    worker_view = models.IntegerField(default='0')
    expert_view = models.IntegerField(default='0')
    serviceman_view = models.IntegerField(default='0')


    class Meta:
        db_table = 'request'

class RequestImage(models.Model):
    req_id = models.CharField(max_length=20, default='0102')
    image = models.ImageField(upload_to="requests/")

    class Meta:
        db_table = 'requestimage'

class Notification(models.Model):
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)
    not_id = models.ForeignKey(Requests, on_delete=models.CASCADE)
    request = models.CharField(max_length=200, default='Request')
    title = models.CharField(max_length=350, default='title')
    description = models.TextField(default='Description')
    not_sender = models.CharField(max_length=50, default='Worker')
    not_status = models.CharField(max_length=100, default='Status')
    not_date = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        db_table = 'notification'


