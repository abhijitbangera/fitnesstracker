from django import forms
from tracker.models import basictracker,bisceptracker,chesttracker,userprofile_extended,backtracker,hiptracker,thightracker

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

class backtrackerForm(forms.ModelForm):
	class Meta:
		model=backtracker
		fields = '__all__'
		exclude = ["user"]

class hiptrackerForm(forms.ModelForm):
	class Meta:
		model=hiptracker
		fields = '__all__'
		exclude = ["user"]


class thightrackerForm(forms.ModelForm):
	class Meta:
		model=thightracker
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