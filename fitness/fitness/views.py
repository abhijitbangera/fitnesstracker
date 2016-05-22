from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from tracker.models import basictracker,bisceptracker,chesttracker,userprofile_extended,backtracker,hiptracker,thightracker,shouldertracker,photos
from tracker.forms import basictrackerForm,bisceptrackerForm,chesttrackerForm,userprofile_extended_goalsettings_Form,userprofile_extended_profilesettings_Form,backtrackerForm,hiptrackerForm,thightrackerForm,shouldertrackerForm,photosForm

from instamojo import Instamojo
api = Instamojo(api_key='b01a80d566585ce4c10fd76e72ee052d',
                auth_token='3d03b6076af55593df904d15f255a3e6',
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

def payment(request):

	# response = api.link_create(title='Hello, world1!',
 #                           description='Well, hello again.',
 #                           base_price=0)
	# print(response)

	# print (response['link'])

	response = api.payment_request_status('MOJO6519000F07999514')
	print(response)
	print (response['payment_request']['shorturl'])  # Get the short URL
	print (response['payment_request']['status'] )   # Get the current status
	print (response['payment_request']['payments'])  # List of payments
	return render(request, "loggedin_homepage.html", {})
