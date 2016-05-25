from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from tracker.models import basictracker,bisceptracker,chesttracker,userprofile_extended,backtracker,hiptracker,thightracker,shouldertracker,photos
from tracker.forms import basictrackerForm,bisceptrackerForm,chesttrackerForm,userprofile_extended_goalsettings_Form,userprofile_extended_profilesettings_Form,backtrackerForm,hiptrackerForm,thightrackerForm,shouldertrackerForm,photosForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from instamojo import Instamojo
api = Instamojo(api_key='',
                auth_token='',
                endpoint='https://test.instamojo.com/api/1.1/')


@login_required
def homepage(request):
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
			'form':form,}
	return render(request, "loggedin_homepage.html", context)


@login_required
def test(request):
	username=request.user
	
	context={'username':str(username).title(),
			'username_original':username,
			}
	return render(request, "user_weighttracker.html", context)

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response



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

	# response = api.link_create(title='Hello, world1!',
 #                           description='Well, hello again.',
 #                           base_price=0)
	# print(response)

	# print (response['link'])

	response = api.payment_request_create(
    amount='3499',
    purpose='FIFA 16',
    send_email=True,
    email="foo@example.com",
    redirect_url="http://127.0.0.1:8000/payment/"
    )

	# print the long URL of the payment request.
	print (response['payment_request']['longurl'])
	# print the unique ID(or payment request ID)
	print (response['payment_request']['id'])
	id1=response['payment_request']['id']
	print(api.payment_request_payment_status(id1,'MOJO6519000F07999514'))
	return render(request, "loggedin_homepage.html", {})

def payment_confirmation(request):
	url=request
	print(request)
	payment_request_id=request.GET.get('payment_request_id')
	payment_id=request.GET.get('payment_id')
	response=api.payment_request_payment_status(payment_request_id, payment_id)
	print(response['success'])

	return render(request, "payment_confirmation.html", {'response':response})