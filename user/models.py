from django.db import models
from django.utils import timezone
from django import forms


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
    machine_picture = models.ImageField(upload_to='machine/', null=True)
    machine_type = models.CharField(max_length=100, default='Machine')
    machine_status = models.CharField(max_length=100, default='Status')

    class Meta:
        db_table = 'machine'

class Notification(models.Model):
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)
    request = models.CharField(max_length=200, default='Request')
    title = models.CharField(max_length=350, default='title')
    description = models.TextField(default='Description')
    not_status = models.CharField(max_length=100, default='Status')
    not_date = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        db_table = 'notification'
