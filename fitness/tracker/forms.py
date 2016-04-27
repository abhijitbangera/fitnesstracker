from django import forms
from tracker.models import basictracker,bisceptracker,chesttracker,userprofile_extended

class basictrackerForm(forms.ModelForm):
	class Meta:
		model=basictracker
		fields = '__all__'
		exclude = ["user"]

class bisceptrackerForm(forms.ModelForm):
	class Meta:
		model=bisceptracker
		fields = '__all__'
		exclude = ["user"]

class chesttrackerForm(forms.ModelForm):
	class Meta:
		model=chesttracker
		fields = '__all__'
		exclude = ["user"]

class userprofile_extended_goalsettings_Form(forms.ModelForm):
	class Meta:
		model=userprofile_extended
		fields = '__all__'
		exclude = ["mobile","user","age","image"]

class userprofile_extended_profilesettings_Form(forms.ModelForm):
	class Meta:
		model=userprofile_extended
		fields = '__all__'
		exclude = ["gender","user","goal"]