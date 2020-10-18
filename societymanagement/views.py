from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import ListView

from residents.models import Resident

def home(request):
	return redirect('/accounts/login')

def dashboard(request):
	try:
		resident = Resident.objects.get(user=request.user)
	except :
		resident = False
	
	context = {
		'resident':resident
	}
	
	return render(request, "users/dashboard.html",context=context)

