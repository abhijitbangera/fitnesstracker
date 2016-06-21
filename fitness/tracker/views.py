from django.shortcuts import render,get_object_or_404
from tracker.forms import basictrackerForm,bisceptrackerForm,chesttrackerForm,userprofile_extended_goalsettings_Form,userprofile_extended_profilesettings_Form,backtrackerForm,hiptrackerForm,thightrackerForm,shouldertrackerForm,photosForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tracker.models import basictracker,bisceptracker,chesttracker,userprofile_extended,backtracker,hiptracker,thightracker,shouldertracker,photos,subscription
from django.contrib import messages

# Create your views here.
def profile(request,username):

	u = User.objects.get(username=username)
	# username=request.user
	if request.user.is_authenticated():
		template="loggedin_base.html"
		registered_user='yes'
	else:
		template="loggedout_base.html"
		registered_user='no'
	biscep='0'
	chest='0'
	weight='0'
	back='0'
	thigh='0'
	shoulder='0'
	weight_date='///'
	biscep_date='///'
	chest_date='///'
	back_date='///'
	thigh_date='///'
	shoulder_date='///'
	age1='Not Set'
	gender_full='Not Set'
	goal_plan='Not Set'
	about=''
	print(u)
	print(request.user)
	#Weight progress tracker-----------------

	obj=userprofile_extended.objects.filter(user_id=u)
	profilepic1="/media/avatar.png"
	profilepic="/media/avatar.png"
	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic1=i.image.url
	if request.user.is_authenticated():
		obj=userprofile_extended.objects.filter(user_id=request.user)
		profilepic="/media/avatar.png"
		obj_count=obj.count()
		if obj_count>0:
			for i in obj:
				goal_id=i.image
				if goal_id:
					profilepic=i.image.url
	obj = basictracker.objects.filter(user_id=u).order_by('datetime').reverse()[:5]
	w1=[]
	w2=[]

	for i in obj:
		print("Object is:")
		print(i.datetime.date())
		print(i.weight)
		w1.append(str(i.datetime.date()))
		w2.append(i.weight)
	print(len(w1))
	print(w2)
	if len(w1)==0:
		message="No weight record found."
		context7={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,
				'message':message,
				}
		

	elif len(w1)==1:
		context7={'len':1,
				'w10':w1[0],
				'w20':w2[0],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,
				}
	elif len(w1)==2:
		context7={'len':2,
				'w10':w1[0],
				'w20':w2[0],
				'w21':w2[1],
				'w11':w1[1],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,
				}
	elif len(w1)==3:
		context7={'len':3,
				'w10':w1[0],
				'w20':w2[0],
				'w11':w1[1],
				'w21':w2[1],
				'w12':w1[2],
				'w22':w2[2],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,
				}
	elif len(w1)==4:
		context7={'len':4,
				'w10':w1[0],
				'w20':w2[0],
				'w11':w1[1],
				'w21':w2[1],
				'w12':w1[2],
				'w22':w2[2],
				'w13':w1[3],
				'w23':w2[3],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,
				}
	elif len(w1)>4:
		context7={'w10':w1[0],
				'w20':w2[0],
				'w11':w1[1],
				'w21':w2[1],
				'w12':w1[2],
				'w22':w2[2],
				'w13':w1[3],
				'w23':w2[3],
				'w14':w1[4],
				'w24':w2[4],
				'w1':w1,
				'w2':w2,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,}
	obj_bis = bisceptracker.objects.filter(user_id=u).order_by('datetime').reverse()[:5]
	x=[]
	y=[]

	for i in obj_bis:
		print("Object is:")
		print(i.datetime.date())
		print(i.biscep)
		x.append(str(i.datetime.date()))
		y.append(i.biscep)
	print(x)
	print(y)

	if len(x)==0:
		message_biscep="No Biscep record found."
		context1={'username':str(username).title(),
				'username_original':username,
				'message_biscep':message_biscep,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,}
		# context1.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context1)
	elif len(x)==1:
		context1={'len_biscep':1,
				'x0':x[0],
				'y0':y[0],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,
				}
		
	elif len(x)==2:
		context1={'len_biscep':2,
				'x0':x[0],
				'y0':y[0],
				'y1':y[1],
				'x1':x[1],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,
				}
		
	elif len(x)==3:
		context1={'len_biscep':3,
				'x0':x[0],
				'y0':y[0],
				'x1':x[1],
				'y1':y[1],
				'x2':x[2],
				'y2':y[2],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,
				}
		
	elif len(x)==4:
		context1={'len_biscep':4,
				'x0':x[0],
				'y0':y[0],
				'x1':x[1],
				'y1':y[1],
				'x2':x[2],
				'y2':y[2],
				'x3':x[3],
				'y3':y[3],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'profilepic1':profilepic1,
				}
		
	elif len(x)>4:
		context1={'x0':x[0],
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
				'pagetitle': "Profile",
				'profilepic1':profilepic1,	}

	obj1 = chesttracker.objects.filter(user_id=u).order_by('datetime').reverse()[:5]
	a=[]
	b=[]
	for i in obj1:
		print("Object is:")
		print(i.datetime.date())
		print(i.chest)
		a.append(str(i.datetime.date()))
		b.append(i.chest)
	print(a)
	print(b)
	print(len(a))
	print("0000000000000000000000000")
	if len(a)==0:
		message_chest="No Chest record found."
		context8={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'message_chest':message_chest}
		# context.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context)
	elif len(a)==1:
		context8={'len_chest':1,
				'a0':a[0],
				'b0':b[0],
				}
	elif len(a)==2:
		context8={'len_chest':2,
				'a0':a[0],
				'b0':b[0],
				'b1':b[1],
				'a1':a[1],
				}
	elif len(a)==3:
		context8={'len_chest':3,
				'a0':a[0],
				'b0':b[0],
				'a1':a[1],
				'b1':b[1],
				'a2':a[2],
				'b2':b[2],
				}
	elif len(a)==4:
		context8={'len_chest':4,
				'a0':a[0],
				'b0':b[0],
				'a1':a[1],
				'b1':b[1],
				'a2':a[2],
				'b2':b[2],
				'a3':a[3],
				'b3':b[3],
				}
	elif len(a)>4:
		context8={'len_chest':5,
				'a0':a[0],
				'b0':b[0],
				'a1':a[1],
				'b1':b[1],
				'a2':a[2],
				'b2':b[2],
				'a3':a[3],
				'b3':b[3],
				'a4':a[4],
				'b4':b[4],
				'a':a,
				'b':b,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",	}
	

	obj2 = backtracker.objects.filter(user_id=u).order_by('datetime').reverse()[:5]
	c=[]
	d=[]
	for i in obj2:
		print("Object is:")
		print(i.datetime.date())
		print(i.back)
		c.append(str(i.datetime.date()))
		d.append(i.back)
	print(c)
	print(d)
	if len(c)==0:
		message_back="No Back record found."
		context2={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'message_back':message_back}
		# context2.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context2)
	elif len(c)==1:
		context2={'len_back':1,
				'c0':c[0],
				'd0':d[0],
				}
	elif len(c)==2:
		context2={'len_back':2,
				'c0':c[0],
				'd0':d[0],
				'c1':c[1],
				'd1':d[1],
				}
	elif len(c)==3:
		context2={'len_back':3,
				'c0':c[0],
				'd0':d[0],
				'c1':c[1],
				'd1':d[1],
				'c2':c[2],
				'd2':d[2],
				}
	elif len(c)==4:
		context2={'len_back':4,
				'c0':c[0],
				'd0':d[0],
				'c1':c[1],
				'd1':d[1],
				'c2':c[2],
				'd2':d[2],
				'c3':c[3],
				'd3':d[3],
				}
	elif len(c)>4:
		context2={'len_back':5,
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
				'c':c,
				'd':d,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",	}
	

	obj3 = hiptracker.objects.filter(user_id=u).order_by('datetime').reverse()[:5]
	e=[]
	f=[]
	for i in obj3:
		print("Object is:")
		print(i.datetime.date())
		print(i.hip)
		e.append(str(i.datetime.date()))
		f.append(i.hip)
	print(e)
	print(f)
	if len(e)==0:
		message_hip="No Hip record found."
		context3={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'message_hip':message_hip}
		# context3.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context3)
	elif len(e)==1:
		context3={'len_hip':1,
				'e0':e[0],
				'f0':f[0],
				}
	elif len(e)==2:
		context3={'len_hip':2,
				'e0':e[0],
				'f0':f[0],
				'e1':e[1],
				'f1':f[1],
				}
	elif len(e)==3:
		context3={'len_hip':3,
				'e0':e[0],
				'f0':f[0],
				'e1':e[1],
				'f1':f[1],
				'e2':e[2],
				'f2':f[2],
				}
	elif len(e)==4:
		context3={'len_hip':4,
				'e0':ec[0],
				'f0':f[0],
				'e1':e[1],
				'f1':f[1],
				'e2':e[2],
				'f2':f[2],
				'e3':e[3],
				'f3':f[3],
				}
	elif len(e)>4:
		context3={'len_hip':5,
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
				'e':e,
				'f':f,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",	}
	






	obj4 = thightracker.objects.filter(user_id=u).order_by('datetime').reverse()[:5]
	g=[]
	h=[]
	for i in obj4:
		print("Object is:")
		print(i.datetime.date())
		print(i.thigh)
		g.append(str(i.datetime.date()))
		h.append(i.thigh)
	print(g)
	print(h)


	if len(g)==0:
		message_thigh="No Thigh record found."
		context4={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'message_thigh':message_thigh}
		# context4.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context4)
	elif len(g)==1:
		context4={'len_thigh':1,
				'g0':g[0],
				'h0':h[0],
				}
	elif len(g)==2:
		context4={'len_thigh':2,
				'g0':g[0],
				'h0':h[0],
				'g1':g[1],
				'h1':h[1],
				}
	elif len(g)==3:
		context4={'len_thigh':3,
				'g0':g[0],
				'h0':h[0],
				'g1':g[1],
				'h1':h[1],
				'g2':g[2],
				'h2':h[2],
				}
	elif len(g)==4:
		context4={'len_thigh':4,
				'g0':g[0],
				'h0':h[0],
				'g1':g[1],
				'h1':h[1],
				'g2':g[2],
				'h2':h[2],
				'g3':g[3],
				'h3':h[3],
				}
	elif len(g)>4:
		context4={'len_thigh':5,
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
				'g':e,
				'h':h,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",	}


	obj5 = shouldertracker.objects.filter(user_id=u).order_by('datetime').reverse()[:5]
	j=[]
	k=[]
	for i in obj5:
		print("Object is:")
		print(i.datetime.date())
		print(i.shoulder)
		j.append(str(i.datetime.date()))
		k.append(i.shoulder)
	print(j)
	print(k)
	print(len(j))
	print("0000000000000000000000000")
	if len(j)==0:
		message_shoulder="No Shoulder record found."
		context5={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",
				'message_shoulder':message_shoulder}
		# context.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context)
	elif len(j)==1:
		context5={'len_shoulder':1,
				'j0':j[0],
				'k0':k[0],
				}
	elif len(j)==2:
		context5={'len_shoulder':2,
				'j0':j[0],
				'k0':k[0],
				'k1':k[1],
				'j1':j[1],
				}
	elif len(j)==3:
		context5={'len_shoulder':3,
				'j0':j[0],
				'k0':k[0],
				'j1':j[1],
				'k1':k[1],
				'j2':j[2],
				'k2':k[2],
				}
	elif len(j)==4:
		context5={'len_shoulder':4,
				'j0':j[0],
				'k0':k[0],
				'j1':j[1],
				'k1':k[1],
				'j2':j[2],
				'k2':k[2],
				'j3':j[3],
				'k3':k[3],
				}
	elif len(j)>4:
		context5={'len_shoulder':5,
				'j0':j[0],
				'k0':k[0],
				'j1':j[1],
				'k1':k[1],
				'j2':j[2],
				'k2':k[2],
				'j3':j[3],
				'k3':k[3],
				'j4':j[4],
				'k4':k[4],
				'j':j,
				'k':k,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Profile",}

	#end of body progress tracker
	#Photo album code

	obj=photos.objects.filter(user_id=u).order_by('datetime').reverse()[:5]
	photo_list=[]
	photo_list_url=[]
	desc=[]
	for i in obj:
		photo_list.append(i.user_photo)
		photo_list_url.append(i.user_photo.url)
		desc.append(i.description)
	# print(photo_list[0])
	# print(photo_list_url[0])
	# print(desc)
	img1="/media/avatar.png"
	img2="/media/avatar.png"
	img3="/media/avatar.png"
	img4="/media/avatar.png"
	img5="/media/avatar.png"
	desc1=""
	desc2=""
	desc3=""
	desc4=""
	desc5=""
	print(len(photo_list))
	if len(photo_list)==1:
		img1=photo_list_url[0]
		desc1=desc[0]
	elif len(photo_list)==2:
		img1=photo_list_url[0]
		desc1=desc[0]
		img2=photo_list_url[1]
		desc2=desc[1]
	elif len(photo_list)==3:
		img1=photo_list_url[0]
		desc1=desc[0]
		img2=photo_list_url[1]
		desc2=desc[1]
		img3=photo_list_url[2]
		desc3=desc[2]
	elif len(photo_list)==4:
		img1=photo_list_url[0]
		desc1=desc[0]
		img2=photo_list_url[1]
		desc2=desc[1]
		img3=photo_list_url[2]
		desc3=desc[2]
		img4=photo_list_url[3]
		desc4=desc[3]
	elif len(photo_list)>4:
		img1=photo_list_url[0]
		desc1=desc[0]
		img2=photo_list_url[1]
		desc2=desc[1]
		img3=photo_list_url[2]
		desc3=desc[2]
		img4=photo_list_url[3]
		desc4=desc[3]
		img5=photo_list_url[4]
		desc5=desc[4]

	context11={'username':str(username).title(),
			'username_original':username,
			'img1':img1,
			'img2':img2,
			'img3':img3,
			'img4':img4,
			'img5':img5,
			'desc1':desc1,
			'desc2':desc2,
			'desc3':desc3,
			'desc4':desc4,
			'desc5':desc5,
			}





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
	obj4 = backtracker.objects.filter(user_id=u).order_by('datetime').reverse()[:1]
	for i in obj4:
		back=i.back
		back_date=i.datetime.date()
	obj5 = thightracker.objects.filter(user_id=u).order_by('datetime').reverse()[:1]
	for i in obj5:
		thigh=i.thigh
		thigh_date=i.datetime.date()
	obj6 = shouldertracker.objects.filter(user_id=u).order_by('datetime').reverse()[:1]
	for i in obj6:
		shoulder=i.shoulder
		shoulder_date=i.datetime.date()
	obj3=userprofile_extended.objects.filter(user_id=u)
	obj_count=userprofile_extended.objects.filter(user_id=u).count()
	print(obj_count)
	if obj_count>0:
		for i in obj3:
			print(i)
			age1=i.age
			if age1==None:
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
			goal_id=i.image
			if goal_id:
				profilepic1=i.image.url
			about=i.about

		context={'username1':str(username).title(),
				'username_original1':username,
				'username':request.user,
				'biscep':biscep,
				'chest':chest,
				'back':back,
				'weight':weight,
				'thigh':thigh,
				'shoulder':shoulder,
				'weight_date':weight_date,
				'biscep_date':biscep_date,
				'chest_date':chest_date,
				'back_date':back_date,
				'thigh_date':thigh_date,
				'shoulder_date':shoulder_date,
				'age':age1,
				'gender':gender_full,
				'goal':goal_plan,
				'profilepic1':profilepic1,
				'profilepic':profilepic,
				'about':about,
				'template':template,
				'registered_user':registered_user,
				}
		print(context1)
		final_list=dict(list(context7.items()) + list(context1.items())+list(context2.items()) + list(context3.items()) + list(context4.items())+list(context5.items()) + list(context8.items())+list(context11.items()) + list(context.items()))
		return render(request, "user_profile.html", final_list)
	else:
		context={'username1':str(username).title(),
				'username_original1':username,
				'username':request.user,
				'biscep':biscep,
				'chest':chest,
				'back':back,
				'weight':weight,
				'thigh':thigh,
				'shoulder':shoulder,
				'weight_date':weight_date,
				'biscep_date':biscep_date,
				'chest_date':chest_date,
				'back_date':back_date,
				'thigh_date':thigh_date,
				'shoulder_date':shoulder_date,
				'age':"Not Set",
				'gender':"Not Set",
				'goal':"Not Set",
				'about':about,
				'template':template,
				'registered_user':registered_user,
				'profilepic1':profilepic1,
				'profilepic':profilepic,
				}
		final_list=dict( list(context7.items()) + list(context1.items())+list(context2.items()) + list(context3.items()) + list(context4.items())+list(context5.items()) + list(context8.items())+list(context11.items())+ list(context.items()))
		return render(request, "user_profile.html", final_list)


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
			messages.add_message(request,messages.SUCCESS, "Weight Updated successfully")
			return HttpResponseRedirect("/weighttracker/")
	else:
		form=basictrackerForm()
	#Profile pic code ------------------------------
	obj=userprofile_extended.objects.filter(user_id=username)
	profilepic="/media/avatar.png"
	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url

	#-------------------------------------------------------
	context={'username':str(username).title(),
			'username_original':username,
			'pagetitle': "Tracker",
			'profilepic':profilepic}
	context.update(csrf(request))
	form['weight'].label = "Enter your weight (in Kgs)"
	context['form']=form
	return render(request, "user_weighttracker.html", context)

@login_required
def bodytracker(request):
	username=request.user
	obj=userprofile_extended.objects.filter(user_id=username)
	profilepic="/media/avatar.png"
	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url

	if request.method=='POST':
		form= bisceptrackerForm(request.POST)
		form2=chesttrackerForm(request.POST)
		form3=backtrackerForm(request.POST)
		form4=hiptrackerForm(request.POST)
		form5=thightrackerForm(request.POST)
		form6=shouldertrackerForm(request.POST)
		if form.is_valid():
			save_it=form.save(commit = False)
			save_it.user = request.user
			save_it.save()
			print("saved successfully.")
			messages.add_message(request,messages.SUCCESS, "Updated successfully - Biscep size")
			return HttpResponseRedirect("/bodytracker/")
		elif form2.is_valid():
			save_it=form2.save(commit = False)
			save_it.user = request.user
			save_it.save()
			messages.add_message(request,messages.SUCCESS, "Updated successfully - Chest size")
			print("saved successfully.")
			return HttpResponseRedirect("/bodytracker/")
		elif form3.is_valid():
			save_it=form3.save(commit = False)
			save_it.user = request.user
			save_it.save()
			messages.add_message(request,messages.SUCCESS, "Updated successfully - Back size")
			print("saved successfully.")
			return HttpResponseRedirect("/bodytracker/")
		elif form4.is_valid():
			save_it=form4.save(commit = False)
			save_it.user = request.user
			save_it.save()
			messages.add_message(request,messages.SUCCESS, "Updated successfully - Hip size")
			print("saved successfully.")
			return HttpResponseRedirect("/bodytracker/")
		elif form5.is_valid():
			save_it=form5.save(commit = False)
			save_it.user = request.user
			save_it.save()
			messages.add_message(request,messages.SUCCESS, "Updated successfully - Thigh size")
			print("saved successfully.")
			return HttpResponseRedirect("/bodytracker/")
		elif form6.is_valid():
			save_it=form6.save(commit = False)
			save_it.user = request.user
			save_it.save()
			messages.add_message(request,messages.SUCCESS, "Updated successfully - Shoulder size")
			print("saved successfully.")
			print(messages)
			return HttpResponseRedirect("/bodytracker/")
	else:
		form=bisceptrackerForm()
		form2=chesttrackerForm()
		form3=backtrackerForm()
		form4=hiptrackerForm()
		form5=thightrackerForm()
		form6=shouldertrackerForm()

	
	
	form['biscep'].label = "Enter your biscep size (in inches)"
	form2['chest'].label = "Enter your chest size (in inches)"
	form3['back'].label = "Enter your back size (in inches)"
	form4['hip'].label = "Enter your hip size (in inches)"
	form5['thigh'].label = "Enter your thigh size (in inches)"
	form6['shoulder'].label = "Enter your shoulder size (in inches)"
	context={'form':form,
			'form2':form2,
			'form3':form3,
			'form4':form4,
			'form5':form5,
			'form6':form6,
			'username':str(username).title(),
			'username_original':username,
			'pagetitle': "Tracker",
			'profilepic':profilepic}
	context.update(csrf(request))
	return render(request, "user_bodytracker.html", context)

@login_required
def weightprogress(request):
	username=request.user
	obj=userprofile_extended.objects.filter(user_id=username)
	profilepic="/media/avatar.png"
	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url
			
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
				'pagetitle': "Tracker",
				'message':message,
				'profilepic':profilepic}
		context.update(csrf(request))
		form['weight'].label = "Enter your weight (in Kgs)"
		context['form']=form
		return render(request, "user_weighttracker.html", context)

	elif len(x)==1:
		context={'len':1,
				'x0':x[0],
				'y0':y[0],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,
				}
	elif len(x)==2:
		context={'len':2,
				'x0':x[0],
				'y0':y[0],
				'y1':y[1],
				'x1':x[1],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,
				}
	elif len(x)==3:
		context={'len':3,
				'x0':x[0],
				'y0':y[0],
				'x1':x[1],
				'y1':y[1],
				'x2':x[2],
				'y2':y[2],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,
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
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,
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
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,	}
	return render(request, "user_weightprogress.html", context)

@login_required
def bodyprogress(request):
	username=request.user
	obj=userprofile_extended.objects.filter(user_id=username)
	profilepic="/media/avatar.png"
	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url
	obj = bisceptracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	x=[]
	y=[]
	for i in obj:
		print("Object is:")
		print(i.datetime.date())
		print(i.biscep)
		x.append(str(i.datetime.date()))
		y.append(i.biscep)
	print(x)
	print(y)

	if len(x)==0:
		message_biscep="No Biscep record found. Please update your Biscep size in tracker."
		context1={'username':str(username).title(),
				'username_original':username,
				'message_biscep':message_biscep,
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,}
		# context1.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context1)
	elif len(x)==1:
		context1={'len_biscep':1,
				'x0':x[0],
				'y0':y[0],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,
				}
		
	elif len(x)==2:
		context1={'len_biscep':2,
				'x0':x[0],
				'y0':y[0],
				'y1':y[1],
				'x1':x[1],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,
				}
		
	elif len(x)==3:
		context1={'len_biscep':3,
				'x0':x[0],
				'y0':y[0],
				'x1':x[1],
				'y1':y[1],
				'x2':x[2],
				'y2':y[2],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,
				}
		
	elif len(x)==4:
		context1={'len_biscep':4,
				'x0':x[0],
				'y0':y[0],
				'x1':x[1],
				'y1':y[1],
				'x2':x[2],
				'y2':y[2],
				'x3':x[3],
				'y3':y[3],
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,
				}
		
	elif len(x)>4:
		context1={'x0':x[0],
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
				'pagetitle': "Progress Tracker",
				'profilepic':profilepic,	}
		# return render(request, "user_bodyprogress.html", context1)


	obj1 = chesttracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	a=[]
	b=[]
	for i in obj1:
		print("Object is:")
		print(i.datetime.date())
		print(i.chest)
		a.append(str(i.datetime.date()))
		b.append(i.chest)
	print(a)
	print(b)
	print(len(a))
	print("0000000000000000000000000")
	if len(a)==0:
		message_chest="No Chest record found. Please update your Chest size in tracker."
		context={'username':str(username).title(),
				'username_original':username,
				'pagetitle': " Progress Tracker",
				'message_chest':message_chest}
		# context.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context)
	elif len(a)==1:
		context={'len_chest':1,
				'a0':a[0],
				'b0':b[0],
				'username_original':username,
				}
	elif len(a)==2:
		context={'len_chest':2,
				'a0':a[0],
				'b0':b[0],
				'b1':b[1],
				'a1':a[1],
				'username_original':username,
				}
	elif len(a)==3:
		context={'len_chest':3,
				'a0':a[0],
				'b0':b[0],
				'a1':a[1],
				'b1':b[1],
				'a2':a[2],
				'b2':b[2],
				'username_original':username,
				}
	elif len(a)==4:
		context={'len_chest':4,
				'a0':a[0],
				'b0':b[0],
				'a1':a[1],
				'b1':b[1],
				'a2':a[2],
				'b2':b[2],
				'a3':a[3],
				'b3':b[3],
				'username_original':username,
				}
	elif len(a)>4:
		context={'len_chest':5,
				'a0':a[0],
				'b0':b[0],
				'a1':a[1],
				'b1':b[1],
				'a2':a[2],
				'b2':b[2],
				'a3':a[3],
				'b3':b[3],
				'a4':a[4],
				'b4':b[4],
				'a':a,
				'b':b,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'username_original':username,	}
	

	obj2 = backtracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	c=[]
	d=[]
	for i in obj2:
		print("Object is:")
		print(i.datetime.date())
		print(i.back)
		c.append(str(i.datetime.date()))
		d.append(i.back)
	print(c)
	print(d)
	if len(c)==0:
		message_back="No Back record found. Please update your Back size in tracker."
		context2={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'message_back':message_back}
		# context2.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context2)
	elif len(c)==1:
		context2={'len_back':1,
				'c0':c[0],
				'd0':d[0],
				}
	elif len(c)==2:
		context2={'len_back':2,
				'c0':c[0],
				'd0':d[0],
				'c1':c[1],
				'd1':d[1],
				}
	elif len(c)==3:
		context2={'len_back':3,
				'c0':c[0],
				'd0':d[0],
				'c1':c[1],
				'd1':d[1],
				'c2':c[2],
				'd2':d[2],
				}
	elif len(c)==4:
		context2={'len_back':4,
				'c0':c[0],
				'd0':d[0],
				'c1':c[1],
				'd1':d[1],
				'c2':c[2],
				'd2':d[2],
				'c3':c[3],
				'd3':d[3],
				}
	elif len(c)>4:
		context2={'len_back':5,
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
				'c':c,
				'd':d,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",	}
	

	obj3 = hiptracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	e=[]
	f=[]
	for i in obj3:
		print("Object is:")
		print(i.datetime.date())
		print(i.hip)
		e.append(str(i.datetime.date()))
		f.append(i.hip)
	print(e)
	print(f)
	if len(e)==0:
		message_hip="No Hip record found. Please update your Hip size in tracker."
		context3={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'message_hip':message_hip}
		# context3.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context3)
	elif len(e)==1:
		context3={'len_hip':1,
				'e0':e[0],
				'f0':f[0],
				}
	elif len(e)==2:
		context3={'len_hip':2,
				'e0':e[0],
				'f0':f[0],
				'e1':e[1],
				'f1':f[1],
				}
	elif len(e)==3:
		context3={'len_hip':3,
				'e0':e[0],
				'f0':f[0],
				'e1':e[1],
				'f1':f[1],
				'e2':e[2],
				'f2':f[2],
				}
	elif len(e)==4:
		context3={'len_hip':4,
				'e0':ec[0],
				'f0':f[0],
				'e1':e[1],
				'f1':f[1],
				'e2':e[2],
				'f2':f[2],
				'e3':e[3],
				'f3':f[3],
				}
	elif len(e)>4:
		context3={'len_hip':5,
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
				'e':e,
				'f':f,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",	}
	






	obj4 = thightracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	g=[]
	h=[]
	for i in obj4:
		print("Object is:")
		print(i.datetime.date())
		print(i.thigh)
		g.append(str(i.datetime.date()))
		h.append(i.thigh)
	print(g)
	print(h)


	if len(g)==0:
		message_thigh="No Thigh record found. Please update your Thigh size in tracker."
		context4={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'message_thigh':message_thigh}
		# context4.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context4)
	elif len(g)==1:
		context4={'len_thigh':1,
				'g0':g[0],
				'h0':h[0],
				}
	elif len(g)==2:
		context4={'len_thigh':2,
				'g0':g[0],
				'h0':h[0],
				'g1':g[1],
				'h1':h[1],
				}
	elif len(g)==3:
		context4={'len_thigh':3,
				'g0':g[0],
				'h0':h[0],
				'g1':g[1],
				'h1':h[1],
				'g2':g[2],
				'h2':h[2],
				}
	elif len(g)==4:
		context4={'len_thigh':4,
				'g0':g[0],
				'h0':h[0],
				'g1':g[1],
				'h1':h[1],
				'g2':g[2],
				'h2':h[2],
				'g3':g[3],
				'h3':h[3],
				}
	elif len(g)>4:
		context4={'len_thigh':5,
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
				'g':e,
				'h':h,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",	}


	obj5 = shouldertracker.objects.filter(user_id=request.user).order_by('datetime').reverse()[:5]
	j=[]
	k=[]
	for i in obj5:
		print("Object is:")
		print(i.datetime.date())
		print(i.shoulder)
		j.append(str(i.datetime.date()))
		k.append(i.shoulder)
	print(j)
	print(k)
	print(len(j))
	print("0000000000000000000000000")
	if len(j)==0:
		message_shoulder="No Shoulder record found. Please update your Shoulder size in tracker."
		context5={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",
				'message_shoulder':message_shoulder}
		# context.update(csrf(request))
		# return render(request, "user_bodyprogress.html", context)
	elif len(j)==1:
		context5={'len_shoulder':1,
				'j0':j[0],
				'k0':k[0],
				}
	elif len(j)==2:
		context5={'len_shoulder':2,
				'j0':j[0],
				'k0':k[0],
				'k1':k[1],
				'j1':j[1],
				}
	elif len(j)==3:
		context5={'len_shoulder':3,
				'j0':j[0],
				'k0':k[0],
				'j1':j[1],
				'k1':k[1],
				'j2':j[2],
				'k2':k[2],
				}
	elif len(j)==4:
		context5={'len_shoulder':4,
				'j0':j[0],
				'k0':k[0],
				'j1':j[1],
				'k1':k[1],
				'j2':j[2],
				'k2':k[2],
				'j3':j[3],
				'k3':k[3],
				}
	elif len(j)>4:
		context5={'len_shoulder':5,
				'j0':j[0],
				'k0':k[0],
				'j1':j[1],
				'k1':k[1],
				'j2':j[2],
				'k2':k[2],
				'j3':j[3],
				'k3':k[3],
				'j4':j[4],
				'k4':k[4],
				'j':j,
				'k':k,
				'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Progress Tracker",	}
	
	# print(context)
	# print(context1)
	# print(context2)
	print(context4)
	final_list=dict(list(context.items()) + list(context1.items()) + list(context2.items())+ list(context3.items()) + list(context4.items())+ list(context5.items()))
	print(final_list)
	return render(request, "user_bodyprogress.html", final_list)



def goal_settings(request):
	username=request.user
	profilepic="/media/avatar.png"
	obj=userprofile_extended.objects.filter(user_id=request.user)
	obj_count=obj.count()
	a=None
	
	if obj_count>0:
		a=userprofile_extended.objects.get(user_id=request.user)
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url
	
	if request.method=='POST':
		if userprofile_extended.objects.filter(user_id=request.user):
			userprofile_instance=userprofile_extended.objects.get(user_id=request.user)
			form= userprofile_extended_goalsettings_Form(request.POST, instance=userprofile_instance)
			obj=userprofile_extended.objects.filter(user_id=request.user)
			obj_count=obj.count()
			
			print("yes at goal settings............")
			if form.is_valid():
				save_it=form.save(commit = False)
				save_it.user = request.user
				plan_selected=save_it.goal
				if plan_selected=='1':
					trainer='plan1_trainer'
					nutritionist='plan1_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist
				elif plan_selected=='2':
					trainer='plan2_trainer'
					nutritionist='plan2_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist
				elif plan_selected=='3':
					trainer='plan3_trainer'
					nutritionist='plan3_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist
				elif plan_selected=='4':
					trainer='plan4_trainer'
					nutritionist='plan4_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist
				else:
					trainer='plan1_trainer'
					nutritionist='plan1_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist

				supplimentexpert='supplimentexpert'
				contact='info'
				save_it.supplimentexpert=supplimentexpert
				save_it.contact=contact

				save_it.save(update_fields=["gender","goal","trainer","nutritionist","supplimentexpert","contact","about"])
				print("saved successfully.1")
				return HttpResponseRedirect("/")
		else:
			form= userprofile_extended_goalsettings_Form(request.POST)
			if form.is_valid():
				save_it=form.save(commit = False)
				save_it.user = request.user
				plan_selected=save_it.goal
				if plan_selected=='1':
					trainer='plan1_trainer'
					nutritionist='plan1_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist
				elif plan_selected=='2':
					trainer='plan2_trainer'
					nutritionist='plan2_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist
				elif plan_selected=='3':
					trainer='plan3_trainer'
					nutritionist='plan3_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist
				elif plan_selected=='4':
					trainer='plan4_trainer'
					nutritionist='plan4_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist
				else:
					trainer='plan1_trainer'
					nutritionist='plan1_nutritionist'
					save_it.trainer=trainer
					save_it.nutritionist=nutritionist

				supplimentexpert='supplimentexpert'
				contact='info'
				save_it.supplimentexpert=supplimentexpert
				save_it.contact=contact
				save_it.save()
				print("saved successfully.2")
				return HttpResponseRedirect("/")
	else:
		form=userprofile_extended_goalsettings_Form(instance=a)
	context={'username':str(username).title(),
			'username_original':username,
			'pagetitle': "Goal Setting",
			'form':form,
			'profilepic':profilepic}
	context.update(csrf(request))

	return render(request, "user_goal_settings.html", context)

def profile_settings(request):
	profilepic="/media/avatar.png"
	username=request.user
	obj=userprofile_extended.objects.filter(user_id=request.user)
	obj_count=obj.count()
	a=None
	if obj_count>0:
		a=userprofile_extended.objects.get(user_id=request.user)
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url
	if request.method=='POST':
		if userprofile_extended.objects.filter(user_id=request.user):
			userprofile_instance=userprofile_extended.objects.get(user_id=request.user)
			form= userprofile_extended_profilesettings_Form(request.POST or None,request.FILES or None, instance=userprofile_instance )
			# profilepic=i.image.url
			print("yes............")
			if form.is_valid():
				save_it=form.save(commit = False)
				save_it.user = request.user
				save_it.save(update_fields=["mobile","age","image","about"])
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
		form=userprofile_extended_profilesettings_Form(instance=a)
	context={'username':str(username).title(),
			'username_original':username,
			'pagetitle': "Profile Settings",
			'form':form,
			'profilepic':profilepic}
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


@login_required
def photosView(request):
	profilepic="/media/avatar.png"
	username=request.user
	if request.method=='POST':
		# if photos.objects.filter(user_id=request.user):
		# 	photos_instance=photos.objects.get(user_id=request.user)
		# 	form= photosForm(request.POST or None,request.FILES or None, instance=photos_instance )
		# 	obj=photos.objects.filter(user_id=username)
		# 	print("yes............")
		# 	print(obj.count())
		# 	if form.is_valid():
		# 		save_it=form.save(commit = False)
		# 		save_it.user = request.user
				
		# 		save_it.save(update_fields=["user_photo","datetime","user_id"])
		# 		print("updated successfully.")
		# 		return HttpResponseRedirect("/")
		# else:
		form= photosForm(request.POST or None,request.FILES or None)
		if form.is_valid():
			save_it=form.save(commit = False)
			save_it.user = request.user
			
			save_it.save()
			print("saved successfully.")
			return HttpResponseRedirect("/")
	else:
		form=photosForm()
		obj=photos.objects.filter(user_id=username).order_by('datetime').reverse()[:5]

		photo_list=[]
		photo_list_url=[]
		desc=[]
		dnt=[]
		obj2=userprofile_extended.objects.filter(user_id=username)
		profilepic="/media/avatar.png"
		obj_count=obj2.count()
		if obj_count>0:
			for i in obj2:
				goal_id=i.image
				if goal_id:
					profilepic=i.image.url

		for i in obj:
			# profilepic=i.image.url
			photo_list.append(i.user_photo)
			photo_list_url.append(i.user_photo.url)
			desc.append(i.description)
			dnt.append(i.datetime)
	# print(photo_list[0])
	# print(photo_list_url[0])
	# print(dnt)
	img1="/media/avatar.png"
	img2="/media/avatar.png"
	img3="/media/avatar.png"
	img4="/media/avatar.png"
	img5="/media/avatar.png"
	desc1=""
	desc2=""
	desc3=""
	desc4=""
	desc5=""
	dnt1=""
	dnt2=""
	dnt3=""
	dnt4=""
	dnt5=""
	print(len(photo_list))
	if len(photo_list)==1:
		img1=photo_list_url[0]
		desc1=desc[0]
		dnt1=dnt[0]
	elif len(photo_list)==2:
		img1=photo_list_url[0]
		desc1=desc[0]
		dnt1=dnt[0]
		img2=photo_list_url[1]
		desc2=desc[1]
		dnt2=dnt[1]
	elif len(photo_list)==3:
		img1=photo_list_url[0]
		desc1=desc[0]
		dnt1=dnt[0]
		img2=photo_list_url[1]
		desc2=desc[1]
		dnt2=dnt[1]
		img3=photo_list_url[2]
		desc3=desc[2]
		dnt3=dnt[2]
	elif len(photo_list)==4:
		img1=photo_list_url[0]
		desc1=desc[0]
		dnt1=dnt[0]
		img2=photo_list_url[1]
		desc2=desc[1]
		dnt2=dnt[1]
		img3=photo_list_url[2]
		desc3=desc[2]
		dnt3=dnt[2]
		img4=photo_list_url[3]
		desc4=desc[3]
		dnt4=dnt[3]
	elif len(photo_list)>4:
		img1=photo_list_url[0]
		desc1=desc[0]
		dnt1=dnt[0]
		img2=photo_list_url[1]
		desc2=desc[1]
		dnt2=dnt[1]
		img3=photo_list_url[2]
		desc3=desc[2]
		dnt3=dnt[2]
		img4=photo_list_url[3]
		desc4=desc[3]
		dnt4=dnt[3]
		img5=photo_list_url[4]
		desc5=desc[4]
		dnt5=dnt[4]
	
	# a=userprofile_extended.objects.get(user_id=request.user)
	
	context={'username':str(username).title(),
			'username_original':username,
			'pagetitle': "Photos",
			'form':form,
			'img1':img1,
			'img2':img2,
			'img3':img3,
			'img4':img4,
			'img5':img5,
			'desc1':desc1,
			'desc2':desc2,
			'desc3':desc3,
			'desc4':desc4,
			'desc5':desc5,
			'dnt1':dnt1,
			'dnt2':dnt2,
			'dnt3':dnt3,
			'dnt4':dnt4,
			'dnt5':dnt5,
			'profilepic':profilepic,
			}


	return render(request, "photos.html", context)

@login_required
def photodelete(request,id):
	print(request.user.id)
	print(get_object_or_404(photos, user_photo="./"+id).user_id)
	if request.user.id==get_object_or_404(photos, user_photo="./"+id).user_id:
		note = get_object_or_404(photos, user_photo="./"+id).delete()
	return HttpResponseRedirect("/photos")