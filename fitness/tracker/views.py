from django.shortcuts import render,get_object_or_404
from tracker.forms import basictrackerForm,bisceptrackerForm,chesttrackerForm,userprofile_extended_goalsettings_Form,userprofile_extended_profilesettings_Form,backtrackerForm,hiptrackerForm,thightrackerForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from tracker.models import basictracker,bisceptracker,chesttracker,userprofile_extended,backtracker,hiptracker,thightracker
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
		form3=backtrackerForm(request.POST)
		form4=hiptrackerForm(request.POST)
		form5=thightrackerForm(request.POST)
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
		elif form3.is_valid():
			save_it=form3.save(commit = False)
			save_it.user = request.user
			save_it.save()
			print("saved successfully.")
			return HttpResponseRedirect("/")
		elif form4.is_valid():
			save_it=form4.save(commit = False)
			save_it.user = request.user
			save_it.save()
			print("saved successfully.")
			return HttpResponseRedirect("/")
		elif form5.is_valid():
			save_it=form5.save(commit = False)
			save_it.user = request.user
			save_it.save()
			print("saved successfully.")
			return HttpResponseRedirect("/")
	else:
		form=bisceptrackerForm()
		form2=chesttrackerForm()
		form3=backtrackerForm()
		form4=hiptrackerForm()
		form5=thightrackerForm()

	
	
	form['biscep'].label = "Enter your biscep size"
	form2['chest'].label = "Enter your chest size"
	form3['back'].label = "Enter your back size"
	form4['hip'].label = "Enter your hip size"
	form5['thigh'].label = "Enter your thigh size"
	context={'form':form,
			'form2':form2,
			'form3':form3,
			'form4':form4,
			'form5':form5,
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
	print(len(x))
	print(y)
	if len(x)==0:
		message="You haven't updated your weight details in your profile. Please enter your weight below:"
		
		username=request.user
		if request.method=='POST':
			form= basictrackerForm(request.POST)
			if form.is_valid():
				save_it=form.save(commit = False)
				save_it.user = request.user
				save_it.save()
				print("saved successfully.")
				return HttpResponseRedirect("")
		else:
			form=basictrackerForm()

		context={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Weight Tracker",
				'message':message}
		context.update(csrf(request))
		form['weight'].label = "Enter your weight"
		context['form']=form
		return render(request, "user_weighttracker.html", context)

	elif len(x)==1:
		context={'len':1,
				'x0':x[0],
				'y0':y[0],
				}
	elif len(x)==2:
		context={'len':2,
				'x0':x[0],
				'y0':y[0],
				'y1':y[1],
				'x1':x[1],
				}
	elif len(x)==3:
		context={'len':3,
				'x0':x[0],
				'y0':y[0],
				'x1':x[1],
				'y1':y[1],
				'x2':x[2],
				'y2':y[2],
				}
	elif len(x)==4:
		context={'len':4,
				'x0':x[0],
				'y0':y[0],
				'x1':x[1],
				'y1':y[1],
				'x2':x[2],
				'y2':y[2],
				'x3':x[3],
				'y3':y[3],
				}
	else:

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

	obj2 = backtracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	c=[]
	d=[]
	for i in obj2:
		print("Object is:")
		print(i.datetime.date())
		print(i.back)
		c.append(str(i.datetime.date()).replace("-",", "))
		d.append(i.back)
	print(c)
	print(d)

	obj3 = hiptracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	e=[]
	f=[]
	for i in obj3:
		print("Object is:")
		print(i.datetime.date())
		print(i.hip)
		e.append(str(i.datetime.date()).replace("-",", "))
		f.append(i.hip)
	print(e)
	print(f)

	obj4 = thightracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	g=[]
	h=[]
	for i in obj4:
		print("Object is:")
		print(i.datetime.date())
		print(i.thigh)
		g.append(str(i.datetime.date()).replace("-",", "))
		h.append(i.thigh)
	print(g)
	print(h)

	print(len(x))
	print(y)
	if len(x)==0 and len(a)==0:
		message_bis="Update the details"
		message_chest="Update the details"
		context={'message_bis':message_bis,
			'message_chest':message_chest}
	
	else:

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
				'c0':c[0],
				'd0':d[0],
				'c1':c[1],
				'd1':d[1],
				'c2':c[2],
				'd2':d[2],
				'c3':c[3],
				'd3':d[3],
				'c4':c[4],
				'd4':d[4],	
				'e0':e[0],
				'f0':f[0],
				'e1':e[1],
				'f1':f[1],
				'e2':e[2],
				'f2':f[2],
				'e3':e[3],
				'f3':f[3],
				'e4':e[4],
				'f4':f[4],
				'g0':g[0],
				'h0':h[0],
				'g1':g[1],
				'h1':h[1],
				'g2':g[2],
				'h2':h[2],
				'g3':g[3],
				'h3':h[3],
				'g4':g[4],
				'h4':h[4],
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
