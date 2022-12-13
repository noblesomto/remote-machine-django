from django.db import models
from datetime import datetime
from user.models import Machine, User

# Create your models here.
class Expert_chat(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)
    message = models.TextField(default='Description Message')
    chat_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        db_table = 'expert_chat'