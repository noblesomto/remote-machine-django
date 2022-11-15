# Generated by Django 4.1.3 on 2022-11-15 18:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('worker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='Description Message')),
                ('chat_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('machine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.machine')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'chat',
            },
        ),
    ]
