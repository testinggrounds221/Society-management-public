from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import render
from .models import Resident,Invoice,Receipt
from django.utils import timezone
import datetime

from residents.mail import send_email
import environ

env = environ.Env()
environ.Env.read_env()

mail_service_enabled = (env('MAILSERVICE') == 'TRUE')

def get_resident(request):
	"""
	Method to check whether the current user is a resident or not
	If not a resident then redirects to dashboard
	"""
	try:
		resident = Resident.objects.get(user=request.user)
		return resident
	except:
		return False

def get_invoice(invoice_id):
	"""
	Method that returns the invoice for the specified invoice_id
	"""
	return Invoice.objects.get(id = invoice_id) 

def get_receipt(request,invoice_id):
	"""
	Method that returns the Receipt object for the invoice_id and the current authenticated user
	Returns Error object is nothing is found
	"""
	try:
		rec = Receipt.objects.get(user=request.user,invoice=invoice_id)
	except:
		rec = {
			'error':'No Receipt For the given receipt id and current user'
		}
	return rec
	
def get_fee(request,invoice_id,resident):
	"""
	Method that returns the Fee to be paid for the respective invoice_id and resident object as a dictionary
	"""
	inv = get_invoice(invoice_id) # Invoice Object
	
	days = (datetime.date.today() - inv.due_date).days # Time elapsed from due date
	
	fee_particulars = resident.get_amount() # Fee particulars for respective Block

	if days <= 0:
		late_fee = 0
	else:
		late_fee = days * fee_particulars['late']
	fee_particulars['late_fee'] = late_fee
	fee_particulars['late_by_days'] = days
	return fee_particulars

def user_page(request):
	"""
	Page to display the User's profile and Unpaid Invoices
	It also provides the template with resident information of the authenticated user
	"""
	res = get_resident(request)
	if not res:
		return HttpResponseRedirect("/dashboard")
	else:
		resident = res
	context = {
		'resident':resident,
		'unpaid_invoice_ids': resident.get_unpaid_invoice_ids(),
		'unpaid_invoice_objects': resident.get_unpaid_invoice_objects(),
	}
	return render(request,'user_page.html',context)
	# return HttpResponse(JsonResponse(context))

def payment_page(request,invoice_id):
	"""
	Page to Display the Amount due to the customer with late fee
	"""
	res = get_resident(request)# Resident Object

	if not res:
		return HttpResponseRedirect("/dashboard")
	else:
		resident = res
	if res.check_paid(invoice_id):
		print("Already Paid")
	
	context = get_fee(request,invoice_id,resident)
	context['grand_total'] = context['late_fee'] + context['invoice_total']
	context['invoice_id'] = invoice_id
	# return HttpResponse(JsonResponse(context))
	return render(request,'payment_page.html',context)
	
def receipt_page(request,receipt_id):
	"""
	Page to Display the receipt and also redirected page if already paid
	"""
	res = get_resident(request)# Resident Object
	if not res:
		return HttpResponseRedirect("/dashboard")
	try:
		rec = Receipt.objects.get(pk=receipt_id)
		send_email(rec,res)
	except:
		rec = {
			'error':'No Receipt matching the ID'
			}
	
	context = {
		'resident': res,
		'receipt' : rec
	}
	# return HttpResponse(JsonResponse(res))
	
	return render(request,'receipts/receipt_detail.html',context)
	
def generate_receipt(request,invoice_id):
	"""
	URL to Create the receipt and redirects to the Receipts page
	"""
	res = get_resident(request)# Resident Object
	if not res:
		return HttpResponseRedirect("/dashboard")
	else:
		resident = res
	fee_particulars = get_fee(request,invoice_id,resident)

	inv = get_invoice(invoice_id)
	rec = Receipt(
		user=request.user,
		title=inv.title,
		invoice=inv, # Keep it as unique in Model Schema
		invoice_fee=fee_particulars['invoice_total'],
		late_fee=fee_particulars['late_fee'],
		total_fee=fee_particulars['late_fee']+fee_particulars['invoice_total'],
		month=inv.month
		)

	rec.save()
	
	return HttpResponseRedirect('{}/paid'.format(invoice_id))

def payment_success(request,invoice_id):
	context = {}
	context['inv'] = get_invoice(invoice_id)
	rec = get_receipt(request,invoice_id)
	res = get_resident(request)
	if mail_service_enabled:
		send_email(rec,res)
	return render(request,'receipts/pay_success.html',context)

def all_receipts(request):
	"""
	Displays the receipts of the user(from user object) Refer societymanagement view 
	"""
	res = get_resident(request)# Resident Object
	if not res:
		return HttpResponseRedirect("/dashboard")
	else:
		resident = res

	paid_receipt_ids = [x[0] for x in Receipt.objects.all().filter(user=request.user).values_list('id')]
	obj_list = []
	for ui_id in paid_receipt_ids:
		obj_list.append(Receipt.objects.get(id = ui_id))
		
	context = {
		'receipts':obj_list
	}

	return render(request,'receipts/receipt_index.html',context)
