from django.contrib import admin

# Register your models here.
from tracker.models import basictracker,userprofile_extended,photos,subscription

admin.site.register(basictracker)
admin.site.register(userprofile_extended)
admin.site.register(photos)
admin.site.register(subscription)