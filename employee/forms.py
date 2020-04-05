from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
	# role = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
	role = forms.ModelChoiceField(queryset=Group.objects.all())

	class Meta:
		model = User
		fields = [
			'first_name','last_name',
			'email','username','password'
		]

		# excludes = [''] #Either use this of fields = []
		
		label = {
			'password':'Password'
		}

	def __init__(self, *args, **kwargs):

		if kwargs.get('instance'):
			# We get the 'initial' keyword argument or initialize it as a dict if it didn't exist.
			initial = kwargs.setdefault('initial',{})
			# The widget for a ModelMultipleChoiceField expects a list of primary key for selected data
			if kwargs['instance'].groups.all():
				# initial['role'] = [i for i in kwargs['instance'].groups.all()]
				initial['role'] = kwargs['instance'].groups.all()[0] 
				''' This is for single role assigning using ModelChoiceField '''
			else:
				initial['role'] = None
		forms.ModelForm.__init__(self, *args, **kwargs)

	# def clean_email(self):0
	# 	if self.cleaned_data.get('email').endsWith('@gmail.com'):
	# 		return self.cleaned_data.get('email')
	# 	else:
	# 		raise ValidationError('Invalid Email')


	def save(self):
		role_list = []
		password = self.cleaned_data.pop('password')
		role = self.cleaned_data.pop('role')
		# role_list = [i for i in role ]
		u = super().save()
		u.groups.set([role]) 
		''' This is for single role assigning using ModelChoiceField '''
		# u.groups.set(role_list)
		u.set_password(password)
		u.save()

		return u