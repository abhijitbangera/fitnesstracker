from django import forms
from tracker.models import basictracker,bisceptracker,chesttracker

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