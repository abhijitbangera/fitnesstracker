from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from tracker.models import userprofile_extended

@login_required
def homepage(request):
	username=request.user
	obj=userprofile_extended.objects.filter(user_id=username)

	obj_count=obj.count()
	if obj_count>0:
		for i in obj:
			print("-----------")
			print(i.image.url)
			print("-----------")
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
				'pagetitle': "Dashboard",
				'goal':goal_plan,
				'goal_id':goal_id,
				'profilepic':profilepic}
		return render(request, "loggedin_homepage.html", context)
	else:
		context={'username':str(username).title(),
				'username_original':username,
				'pagetitle': "Dashboard",
				'goal':"Not Set",
				'profilepic':"/media/avatar.png"
				}
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