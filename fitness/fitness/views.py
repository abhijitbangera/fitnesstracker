from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
	context={'y':1000}
	return render(request, "plot.html", context)


