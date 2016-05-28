"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'fitness.views.homepage'),
    url(r'^accounts/',include('registration.backends.simple.urls')),
    url(r'^tracker/', 'tracker.views.weighttracker'),
    url(r'^bodytracker/', 'tracker.views.bodytracker'),
    url(r'^plot/', 'tracker.views.plot'),
    url(r'^enroll/', 'fitness.views.payment'),
    url(r'^weighttracker/', 'tracker.views.weighttracker'),
    url(r'^weightprogress/', 'tracker.views.weightprogress'),
    url(r'^bodyprogress/', 'tracker.views.bodyprogress'),
    url(r'^user/(?P<username>[\w.@+-]+)$', 'tracker.views.profile'),
    url(r'^goalsettings/', 'tracker.views.goal_settings'),
    url(r'^profilesettings/', 'tracker.views.profile_settings'),
    # url(r'^messages/', include('django_messages.urls')),
    url(r'^photos/$', 'tracker.views.photosView'),
    url(r'^messages/', include('postman.urls', namespace="postman")),
    url(r'^users/', 'fitness.views.allusers'),
    url(r'^newusers/', 'fitness.views.newusers'),
    url(r'^payment/', 'fitness.views.payment_confirmation'),
    url(r'^photos/delete/media/(?P<id>.+)$','tracker.views.photodelete'),  
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)