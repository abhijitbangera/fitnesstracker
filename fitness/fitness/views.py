from django.shortcuts import render,redirect

def homepage(request):
	context={}
	return render(request, "index.html", context)


