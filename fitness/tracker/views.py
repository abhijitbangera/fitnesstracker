from django.shortcuts import render
from tracker.forms import basictrackerForm,bisceptrackerForm,chesttrackerForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from tracker.models import basictracker,bisceptracker,chesttracker

# Create your views here.
@login_required
def weighttracker(request):
	username=request.user
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

	context={'username':str(username).title(),
			'pagetitle': "Weight Tracker",}
	context.update(csrf(request))
	form['weight'].label = "Enter your weight"
	context['form']=form
	return render(request, "user_weighttracker.html", context)


def bodytracker(request):
	username=request.user
	if request.method=='POST':
		form= bisceptrackerForm(request.POST)
		form2=chesttrackerForm(request.POST)
		if form.is_valid():
			save_it=form.save(commit = False)
			save_it.user = request.user
			save_it.save()
			print("saved successfully.")
			return HttpResponseRedirect("/")
		elif form2.is_valid():
			save_it=form2.save(commit = False)
			save_it.user = request.user
			save_it.save()
			print("saved successfully.")
			return HttpResponseRedirect("/")
	else:
		form=bisceptrackerForm()
		form2=chesttrackerForm()

	
	
	form['biscep'].label = "Enter your biscep size"
	form2['chest'].label = "Enter your chest size"
	context={'form':form,
			'form2':form2,
			'username':str(username).title(),
			'pagetitle': "Body Tracker",}
	context.update(csrf(request))
	return render(request, "user_bodytracker.html", context)

def weightprogress(request):
	username=request.user
	obj = basictracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	x=[]
	y=[]
	for i in obj:
		print("Object is:")
		print(i.datetime.date())
		print(i.weight)
		x.append(str(i.datetime.date()))
		y.append(i.weight)
	print(x)
	print(y)
	
	context={'x0':x[0],
			'y0':y[0],
			'x1':x[1],
			'y1':y[1],
			'x2':x[2],
			'y2':y[2],
			'x3':x[3],
			'y3':y[3],
			'x4':x[4],
			'y4':y[4],
			'username':str(username).title(),
			'pagetitle': "Progress Tracker",	}
	return render(request, "user_weightprogress.html", context)


def bodyprogress(request):
	username=request.user
	obj = bisceptracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	x=[]
	y=[]
	for i in obj:
		print("Object is:")
		print(i.datetime.date())
		print(i.biscep)
		x.append(str(i.datetime.date()).replace("-",", "))
		y.append(i.biscep)
	print(x)
	print(y)

	obj1 = chesttracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	a=[]
	b=[]
	for i in obj1:
		print("Object is:")
		print(i.datetime.date())
		print(i.chest)
		a.append(str(i.datetime.date()).replace("-",", "))
		b.append(i.chest)
	print(a)
	print(b)
	
	context={'a0':a[0],
			'b0':b[0],
			'a1':a[1],
			'b1':b[1],
			'a2':a[2],
			'b2':b[2],
			'a3':a[3],
			'b3':b[3],
			'a4':a[4],
			'b4':b[4],
			'x0':x[0],
			'y0':y[0],
			'x1':x[1],
			'y1':y[1],
			'x2':x[2],
			'y2':y[2],
			'x3':x[3],
			'y3':y[3],
			'x4':x[4],
			'y4':y[4],	
			'username':str(username).title(),
			'pagetitle': "Progress Tracker",	}
	return render(request, "user_bodyprogress.html", context)







def plot(request):
	obj = basictracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
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
	
	context={'x0':x[0],
			'y0':y[0],
			'x1':x[1],
			'y1':y[1],
			'x2':x[2],
			'y2':y[2],
			'x3':x[3],
			'y3':y[3],
			'x4':x[4],
			'y4':y[4],	}
	return render(request, "plot.html", context)
