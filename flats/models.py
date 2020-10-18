from django.contrib.auth.models import User
from django.db import models

class Block(models.Model):
	GROUP_NAMES = (('A','A'),
					('B','B'),
					('C','C'),
					('D','D'))

	group = models.CharField(choices=GROUP_NAMES,unique=True,max_length=2)

	lift_charge = models.IntegerField(default=250)
	garden_charge = models.IntegerField(default=500)
	cleaning_charge = models.IntegerField(default=500)
	water_charge = models.IntegerField(default=750)

	late_charge_per_day = models.IntegerField(default=10)

	total_charge = models.IntegerField(default=2000)
#list1 = [j+str(i) for i in range(37) for j in ['A','B','C','D']]
	def __str__(self):
		return "Block {}".format(self.group)

class House(models.Model):
	NUMBER_CHOICES = [(i,i) for i in range(19)]

	house_block = models.ForeignKey(Block,on_delete=models.CASCADE)
	house_number = models.IntegerField(choices=NUMBER_CHOICES)
	
	tenent_id = models.ForeignKey(User,on_delete=models.DO_NOTHING)


	

