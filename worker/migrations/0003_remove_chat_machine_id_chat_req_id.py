# Generated by Django 4.1.3 on 2022-11-16 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0002_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='machine_id',
        ),
        migrations.AddField(
            model_name='chat',
            name='req_id',
            field=models.CharField(default='0102', max_length=20),
        ),
    ]