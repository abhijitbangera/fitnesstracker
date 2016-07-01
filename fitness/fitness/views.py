from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from tracker.models import basictracker,bisceptracker,chesttracker,userprofile_extended,backtracker,hiptracker,thightracker,shouldertracker,photos,subscription
from tracker.forms import basictrackerForm,bisceptrackerForm,chesttrackerForm,userprofile_extended_goalsettings_Form,userprofile_extended_profilesettings_Form,backtrackerForm,hiptrackerForm,thightrackerForm,shouldertrackerForm,photosForm,subscriptionForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta,timezone
from instamojo import Instamojo
from django.contrib import messages

api = Instamojo(api_key='b01a80d566585ce4c10fd76e72ee052d',
                auth_token='3d03b6076af55593df904d15f255a3e6',
                endpoint='https://test.instamojo.com/api/1.1/')

def indexpage(request):
	context={}
	return render(request, "index.html", context)




def homepage(request):
	if request.user.is_authenticated():
		template="loggedin_base.html"
		registered_user='yes'
	
		date_now = datetime.now(timezone.utc)
		obj=subscription.objects.filter(user_id=request.user)
		for i in obj:
	 		print("*********")
	 		print(i.subscription_startdate)
	 		print(i.expire_days)
	 		days=(date_now-i.subscription_startdate).days
	 		if days>i.expire_days:
	 			defaults={'subscription_status':0}
	 			y=subscription.objects.update_or_create(user_id=request.user.id,defaults=defaults)


		username=request.user
		obj=userprofile_extended.objects.filter(user_id=username)
		form=''
		obj_count=obj.count()
		profilepic="/media/avatar.png"

		form=userprofile_extended_goalsettings_Form()
		goal_plan="Not Set"
		goal_id=''
		if obj_count>0:
			for i in obj:
				# print("-----------")
				# print(i.image.url)
				# print("-----------")
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
					form=userprofile_extended_goalsettings_Form()
				if i.image:
					profilepic=i.image.url
				else:
					profilepic="/media/avatar.png"
		context={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Dashboard",
				'goal':goal_plan,
				'goal_id':goal_id,
				'profilepic':profilepic,
				'form':form,
				'registered_user':registered_user}
	else:
		template="loggedout_base.html"
		registered_user='no'
		context={'registered_user':registered_user,}
		print("not registered user")
	return render(request, "index_check.html", context)


@login_required
def test(request):
	username=request.user
	
	context={'username':str(username).title(),
			'username_original':username,
			}
	return render(request, "user_weighttracker.html", context)




def allusers(request):
	obj=userprofile_extended.objects.filter(user_id=request.user)
	profilepic="/media/avatar.png"
	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url
	user_profile=userprofile_extended.objects.all().order_by('id').reverse()
	paginator = Paginator(user_profile, 10)
	page = request.GET.get('page')
	try:
		users_page = paginator.page(page)
	except PageNotAnInteger:
		users_page = paginator.page(1)
	except EmptyPage:
		users_page = paginator.page(paginator.num_pages)
	print(user_profile)
	user_name=[]
	user_image=[]

	
	context={'users_page':users_page,
			'user_profile':user_profile,
			'profilepic':profilepic,
			'username':request.user,
			}
	return render(request,"users.html",context)


def newusers(request):
	obj=userprofile_extended.objects.filter(user_id=request.user)
	profilepic="/media/avatar.png"
	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url
	
	user_profile=User.objects.all().order_by('id').reverse()
	paginator = Paginator(user_profile, 10)
	page = request.GET.get('page')
	try:
		users_page = paginator.page(page)
	except PageNotAnInteger:
		users_page = paginator.page(1)
	except EmptyPage:
		users_page = paginator.page(paginator.num_pages)
	print(user_profile)
	user_name=[]
	user_image=[]

	
	context={'users_page':users_page,
			'user_profile':user_profile,
			'username':request.user,
			'profilepic':profilepic,
			}
	return render(request,"newusers.html",context)




def payment(request):

	obj=userprofile_extended.objects.filter(user_id=request.user)
	profilepic="/media/avatar.png"
	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url

	response = api.payment_request_create(
    amount='3499',
    purpose='plan1',
    send_email=True,
    email="foo@example.com",
    redirect_url="http://127.0.0.1:8000/payment/"
    )

	plan1=response['payment_request']['longurl']
	# print the long URL of the payment request.
	print (response['payment_request']['longurl'])
	# print the unique ID(or payment request ID)
	print (response['payment_request']['id'])

	context={'plan1':plan1,
			'profilepic':profilepic,
			'username':request.user}
	return render(request, "subscription.html", context)

def payment_confirmation(request):
	obj=userprofile_extended.objects.filter(user_id=request.user)
	profilepic="/media/avatar.png"
	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			goal_id=i.image
			if goal_id:
				profilepic=i.image.url
	url=request
	print(request)
	payment_request_id=request.GET.get('payment_request_id')
	payment_id=request.GET.get('payment_id')
	response=api.payment_request_payment_status(payment_request_id, payment_id)
	print(response['success'])
	print(response['payment_request']['purpose'])
	if response['success']:
		if response['payment_request']['purpose']=='plan1':
			defaults={'expire_days':'15','subscription_status':1,'user_name':request.user.username,'subscription_startdate':datetime.now()}
			y=subscription.objects.update_or_create(user_id=request.user.id,defaults=defaults)
			messages.add_message(request,messages.SUCCESS, "Payment was successful.")
	else:
		messages.add_message(request,messages.ERROR, "Payment Failed.")
	context={'username':request.user,'response':response,'profilepic':profilepic}
	return render(request, "payment_confirmation.html",context)



def bisceps(request):
	return render(request,"workouts_bisceps.html",{})