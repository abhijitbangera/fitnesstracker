from django.shortcuts import render
from tracker.forms import basictrackerForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
# Create your views here.
def basictracker(request):
	if request.POST:
		print("POST HUA!!!!")
		form= basictrackerForm(request.POST)
		if form.is_valid():
			form.save()
			print("saved successfully.")
			return HttpResponseRedirect("/")
	else:
		print("testing")
		form=basictrackerForm()
	context={}
	context.update(csrf(request))
	context['form']=form
	return render(request, "basictracker.html", context)