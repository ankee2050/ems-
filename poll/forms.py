from django import forms
from poll.models import *

class PollForm(forms.ModelForm):
	title = forms.CharField(max_length=255, label='Question')
	
	class Meta:
		model = Question
		fields = ['title']

class ChoiceForm(forms.ModelForm):
	text = forms.CharField(max_length=255, label='Choice')
	
	class Meta:
		model = Choice
		exclude = ('question',)