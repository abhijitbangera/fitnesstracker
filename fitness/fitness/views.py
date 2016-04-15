from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
	username=request.user
	
	context={'username':str(username).title(),
			'pagetitle': "Homepage"}
	return render(request, "loggedin_base.html", context)


@login_required
def test(request):
	username=request.user
	
	context={'username':str(username).title()}
	return render(request, "user_weighttracker.html", context)