from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
	def decorator(view_func):
		def wrap(request, *args, **kwargs):
			if request.role in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrap
	return decorator

def admin_only(view_func):
	def decorator(request, *args, **kwargs):
		if request.role == 'Admin':
			return view_func(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return decorator

def admin_hr_required(view_func):
	def decorator(request, *args, **kwargs):
		if request.role == 'Admin' or request.role == 'HR':
			return view_func(request, *args, **kwargs)
		else:
			raise PermissionDenied
	return decorator