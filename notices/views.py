from django.shortcuts import render,redirect
from .models import Notice


def notice_index(request):
	notices = Notice.objects.all()
	print("in notices view")
	context = {
		'notices':notices
	}
	return render(request,'notice_index.html',context)

def notice_detail(request,pk):
	print("in notice view")
	notice = Notice.objects.get(pk=pk)
	context = {'notice':notice}
	return render(request,'notice_detail.html',context)
