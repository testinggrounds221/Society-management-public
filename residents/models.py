from django.db import models
from django.contrib.auth.models import User
from flats.models import Block

from django.utils import timezone
import datetime

class Resident(models.Model):

	FLAT_NO_CHOICES = [(j+str(i),j+str(i)) for i in range(1,37) for j in ['A','B','C','D']]

	user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
	flat_no = models.CharField(max_length=4,unique=True,choices=FLAT_NO_CHOICES)

	name = models.CharField(max_length=20)
	work = models.CharField(max_length=20,default="Enter Work Here")
	mobile_no = models.CharField(max_length=15,default="Enter Phone Here")
	email_id = models.CharField(max_length=30,default="Enter Email ID Here")
	permanent_address = models.TextField(default="Enter Address Here")
	
	def get_unpaid_invoice_ids(self):
		"""
		Returns a list of unpaid Invoice IDs by the Resident
		"""
		"""
		qry = Invoice.objects.all().values_list('id')
		lst = [x[0] for x in qry]
		"""
		invoice_ids = [x[0] for x in Invoice.objects.all().values_list('id')]
		# qry = Receipt.objects.all().filter(user=self.user).values_list('invoice')
		paid_invoice_ids = [x[0] for x in Receipt.objects.all().filter(user=self.user).values_list('invoice')]

		unpaid_invoice_ids = list(set(invoice_ids).difference(set(paid_invoice_ids)))

		return unpaid_invoice_ids

	def get_unpaid_invoice_objects(self):
		obj_list = []
		for ui_id in self.get_unpaid_invoice_ids():
			obj_list.append(Invoice.objects.get(id = ui_id))
		return obj_list		
	
	def get_amount(self):
		"""
		Returns a dictionary of respective fees
		"""
		flat = self.flat_no
		block = Block.objects.get(group=flat[0]) # not an error
		
		fee = {
			'lift':block.lift_charge,
			'garden':block.garden_charge,
			'clean':block.cleaning_charge,
			'water':block.water_charge,
			'late':block.late_charge_per_day
			}
		invoice_total = fee['lift']+fee['garden']+fee['clean']+fee['water']
		
		fee['invoice_total'] = invoice_total
		
		return fee
	
	def check_paid(self,invoice_id):
		"""
		To check if the current invoice is paid or not
		"""
		paid_invoice_ids = [x[0] for x in Receipt.objects.filter(user=self.user).values_list('invoice')]
		return invoice_id in paid_invoice_ids

	def __str__(self):
		return self.name

MONTH_CHOICES = [("January","January"),("February","February"),("March","March"),("April","April"),("May","May"),("June","June"),("July","July"),
            ("August","August"),("September","September"),("October","October"),("November","November"),("December","December")]

class Invoice(models.Model):
	
	title = models.CharField(max_length=200, default="Maintenance")
	due_date = models.DateField(default=timezone.now()+datetime.timedelta(days=7))
	created_date = models.DateField(default=timezone.now())

	month = models.CharField(max_length=15,choices=MONTH_CHOICES)
	def __str__(self):
		return "Maintenance invoice for the month {}".format(self.month)
	
class Receipt(models.Model):
	
	title = models.CharField(max_length=200, default="maintenence")
	invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	paid_time=models.DateTimeField(default=timezone.now())
	
	invoice_fee = models.IntegerField()
	late_fee = models.IntegerField()
	total_fee = models.IntegerField()
	
	month = models.CharField(max_length=15,choices=MONTH_CHOICES)
	def __str__(self):
		return "Receipt for the month {}".format(self.month)