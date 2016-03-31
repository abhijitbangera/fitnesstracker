from django.shortcuts import render
from tracker.forms import basictrackerForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def basictracker(request):
	if request.method=='POST':
		form= basictrackerForm(request.POST)
		if form.is_valid():
			save_it=form.save(commit = False)
			save_it.user = request.user
			save_it.save()
			print("saved successfully.")
			return HttpResponseRedirect("/")
	else:
		form=basictrackerForm()
	context={}
	context.update(csrf(request))
	context['form']=form
	return render(request, "basictracker.html", context)