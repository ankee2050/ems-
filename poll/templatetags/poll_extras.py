from django import template
from poll.models import Question

register = template.Library()

def upper(value):
	return value.upper()

register.filter('upper',upper)

@register.simple_tag(name='recent_polls')
def recent_polls(n=5, **kwargs):
	"""
		Return recent n polls.
	"""
	name = kwargs.get('name','No argument was passed.')
	questions = Question.objects.all().order_by('-created_at')
	return list(questions)[0:n]