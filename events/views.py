from django.shortcuts import render,redirect
from events.models import Event


def event_index(request):
	events = Event.objects.all()
	context = {
		'events':events
	}
	return render(request,'event_index.html',context)

def event_detail(request,pk):
	event = Event.objects.get(pk=pk)
	context = {'event':event}
	return render(request,'event_detail.html',context)
