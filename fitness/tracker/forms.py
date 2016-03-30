from django import forms
from tracker.models import basictracker

class basictrackerForm(forms.ModelForm):
	class Meta:
		model=basictracker
		fields = '__all__'