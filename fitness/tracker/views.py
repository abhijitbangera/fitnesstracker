from django.shortcuts import render
from tracker.forms import basictrackerForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from tracker.models import basictracker

# Create your views here.
@login_required
def weighttracker(request):
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

def plot(request):
	obj = basictracker.objects.filter(user_id=1).order_by('datetime').reverse()[:5]
	x=[]
	y=[]
	for i in obj:
		print("Object is:")
		print(i.datetime.date())
		print(i.weight)
		x.append(str(i.datetime.date()).replace("-",", "))
		y.append(i.weight)
	print(x)
	print(y)
	context={'x0':x[0].replace("-",", "),
			'y0':y[0],
			'x1':x[1].replace("-",", "),
			'y1':y[1],
			'x2':x[2].replace("-",", "),
			'y2':y[2],
			'x3':x[3].replace("-",", "),
			'y3':y[3],
			'x4':x[4].replace("-",", "),
			'y4':y[4],	}
	return render(request, "plot.html", context)
