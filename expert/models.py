from django.db import models
from datetime import datetime
from user.models import Machine

# Create your models here.
class Instruction(models.Model):
	in_id = models.CharField(max_length=20, default='010203')
	machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)
	x_axis = models.CharField(max_length=250, default='x-axis')
	y_axis = models.CharField(max_length=250, default='y-axis')
	z_axis = models.CharField(max_length=200, default='z-axis')
	machine_speed = models.CharField(max_length=200, default='machine_speed')
	angle = models.CharField(max_length=200, default='angle')
	in_date = models.DateTimeField(default=datetime.now, blank=True)


	class Meta:
		db_table = 'instruction'