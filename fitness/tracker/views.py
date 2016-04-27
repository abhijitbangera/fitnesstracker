from django.shortcuts import render,get_object_or_404
from tracker.forms import basictrackerForm,bisceptrackerForm,chesttrackerForm,userprofile_extended_goalsettings_Form,userprofile_extended_profilesettings_Form
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from tracker.models import basictracker,bisceptracker,chesttracker,userprofile_extended
from django.contrib.auth.models import User

# Create your views here.
def profile(request,username):
	u = User.objects.get(username=username)
	# username=request.user
	print(u)
	obj = basictracker.objects.filter(user_id=u).order_by('datetime').reverse()[:1]
	for i in obj:
		weight=i.weight
		weight_date=i.datetime.date()
	obj1 = bisceptracker.objects.filter(user_id=u).order_by('datetime').reverse()[:1]
	for i in obj1:
		biscep=i.biscep
		biscep_date=i.datetime.date()
	obj2 = chesttracker.objects.filter(user_id=u).order_by('datetime').reverse()[:1]
	for i in obj2:
		chest=i.chest
		chest_date=i.datetime.date()
	obj3=userprofile_extended.objects.filter(user_id=u)
	obj_count=userprofile_extended.objects.filter(user_id=u).count()
	print(obj_count)
	if obj_count>0:
		for i in obj3:
			print(i)
			age1=i.age
			if age1=="":
				age1="Not Set"
			
			gender=i.gender
			if gender=="M":
				gender_full="Male"
			elif gender=="F":
				gender_full="Female"
			else:
				gender_full="Not Set"
			goal_id=i.goal
			if goal_id =="1":
				goal_plan="Weight Loss"
			elif goal_id =="2":
				goal_plan="Mass Gain"
			elif goal_id =="3":
				goal_plan="Lean Muscle Gain"
			elif goal_id =="4":
				goal_plan="Stay Fit"
			else:
				goal_plan="Not Set"
			profilepic=i.image.url
		context={'username':str(username).title(),
				'username_original':username,
				'biscep':biscep,
				'chest':chest,
				'weight':weight,
				'weight_date':weight_date,
				'biscep_date':biscep_date,
				'chest_date':chest_date,
				'age':age1,
				'gender':gender_full,
				'goal':goal_plan,
				'profilepic':profilepic}
		return render(request, "user_profile.html", context)
	else:
		context={'username':str(username).title(),
				'username_original':username,
				'biscep':biscep,
				'chest':chest,
				'weight':weight,
				'weight_date':weight_date,
				'biscep_date':biscep_date,
				'chest_date':chest_date,
				'age':"Not Set",
				'gender':"Not Set",
				'goal':"Not Set"}
		return render(request, "user_profile.html", context)


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
			'username_original':username,
			'pagetitle': "Weight Tracker",}
	context.update(csrf(request))
	form['weight'].label = "Enter your weight"
	context['form']=form
	return render(request, "user_weighttracker.html", context)

@login_required
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
			'username_original':username,
			'pagetitle': "Body Tracker",}
	context.update(csrf(request))
	return render(request, "user_bodytracker.html", context)

@login_required
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
			'x':x,
			'y':y,
			'username':str(username).title(),
			'username_original':username,
			'pagetitle': "Progress Tracker",	}
	return render(request, "user_weightprogress.html", context)

@login_required
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
			'username_original':username,
			'pagetitle': "Progress Tracker",	}
	return render(request, "user_bodyprogress.html", context)


def goal_settings(request):
	username=request.user
	if request.method=='POST':
		if userprofile_extended.objects.filter(user_id=request.user):
			userprofile_instance=userprofile_extended.objects.get(user_id=request.user)
			form= userprofile_extended_goalsettings_Form(request.POST, instance=userprofile_instance)
			print("yes............")
			if form.is_valid():
				save_it=form.save(commit = False)
				save_it.user = request.user
				save_it.save(update_fields=["gender","goal"])
				print("saved successfully.")
				return HttpResponseRedirect("goalsettings/")
		else:
			form= userprofile_extended_goalsettings_Form(request.POST)
			if form.is_valid():
				save_it=form.save(commit = False)
				save_it.user = request.user
				save_it.save()
				print("saved successfully.")
				return HttpResponseRedirect("/")
	else:
		form=userprofile_extended_goalsettings_Form()
	context={'username':str(username).title(),
			'username_original':username,
			'pagetitle': "Weight Tracker",
			'form':form,}
	context.update(csrf(request))

	return render(request, "user_goal_settings.html", context)

def profile_settings(request):
	
	username=request.user
	if request.method=='POST':
		if userprofile_extended.objects.filter(user_id=request.user):
			userprofile_instance=userprofile_extended.objects.get(user_id=request.user)
			form= userprofile_extended_profilesettings_Form(request.POST or None,request.FILES or None, instance=userprofile_instance )
			print("yes............")
			if form.is_valid():
				save_it=form.save(commit = False)
				save_it.user = request.user
				save_it.save(update_fields=["mobile","age","image"])
				print("saved successfully.")
				return HttpResponseRedirect("/")
		else:
			form= userprofile_extended_profilesettings_Form(request.POST or None,request.FILES or None)
			if form.is_valid():
				save_it=form.save(commit = False)
				save_it.user = request.user
				save_it.save()
				print("saved successfully.")
				return HttpResponseRedirect("/")
	else:
		form=userprofile_extended_profilesettings_Form()
	context={'username':str(username).title(),
			'username_original':username,
			'pagetitle': "Weight Tracker",
			'form':form,}
	return render(request, "user_profile_settings.html", context)


@login_required
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
