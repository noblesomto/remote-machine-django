# Generated by Django 4.2 on 2023-04-09 07:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_requests_expert_view_and_more'),
        ('worker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serviceman_chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req_id', models.CharField(default='0102', max_length=20)),
                ('message', models.TextField(default='Description Message')),
                ('chat_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'serviceman_chat',
            },
        ),
    ]