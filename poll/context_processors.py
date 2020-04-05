from poll.models import *


def polls_count(request):
	count = Question.objects.count()
	return {"polls_count":count}