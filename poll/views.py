from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from ems.decorators import admin_only, admin_hr_required
from .forms import *
from .models import *

class PollView(View):
	decorators = [login_required, admin_hr_required]

	@method_decorator(decorators)
	def get(self,request,id=None):
		if id:
			instance = get_object_or_404(Question,id=id)
			poll_form = PollForm(instance=instance)
			choices = instance.choices # choices is property of Question, see models.py
			choice_form = [ChoiceForm(prefix=str(choice.id), instance=choice) for choice in choices ]
			template = 'polls/edit_poll.html'
		else:
			poll_form = PollForm(instance=Question())
			choice_form = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(3)]
			template = 'polls/new_poll.html'
		context = {"poll_form":poll_form, "choice_form":choice_form}
		return render(request, template, context)

	@method_decorator(decorators)
	def post(self, request, id=None):
		if id:
			return self.put(request, id)
		context = {}
		poll_form = PollForm(request.POST or None, instance=Question())
		choice_form = [ChoiceForm(request.POST or None, prefix=str(x), instance=Choice()) for x in range(3)]
		if poll_form.is_valid() and all([cf.is_valid() for cf in choice_form]):
			new_poll = poll_form.save(commit=False)
			new_poll.created_by = request.user
			new_poll.save()
			for cf in choice_form:
				new_choice = cf.save(commit=False)
				new_choice.question = new_poll
				new_choice.save()
			return HttpResponseRedirect(reverse('polls_list'))

	@method_decorator(decorators)
	def put(self, request, id=None):
		context = {}
		instance = get_object_or_404(Question,id=id)
		poll_form = PollForm(request.POST or None, instance=instance)
		choices = instance.choices # choices is property of Question, see models.py
		choice_form = [ChoiceForm(request.POST or None, prefix=str(choice.id), instance=choice) for choice in choices]
		if poll_form.is_valid() and all([cf.is_valid() for cf in choice_form]):
			edit_poll = poll_form.save(commit=False)
			edit_poll.created_by = request.user
			edit_poll.save()
			for cf in choice_form:
				edit_choice = cf.save(commit=False)
				edit_choice.question = edit_poll
				edit_choice.save()
			return HttpResponseRedirect(reverse('polls_list'))
		
		return HttpResponseRedirect(self.request.path_info)

class PollDelete(View):

	decorators = [admin_only]

	def get(self, request, id=None):
		return self.post(request,id)

	@method_decorator(decorators)
	def post(self, request, id=None):
		instance = get_object_or_404(Question,id=id)
		instance.delete()
		return HttpResponseRedirect(reverse('polls_list'))


@login_required(login_url='/login/')
def index(request):
	questions = Question.objects.all()

	context = {
		'title':'Polls',
		'questions':questions
	}
	return render(request, 'polls/index.html', context)

@login_required(login_url='/login/')
def details(request, id=None):
	context = {}
	try:
		question = Question.objects.get(id=id)
	except:
		raise Http404
	context['question'] = question
	return render(request, 'polls/details.html', context)

@login_required(login_url='/login/')
def vote_poll(request, id=None):
	if request.method == 'GET':
		context = {}
		try:
			question = Question.objects.get(id=id)
		except:
			raise Http404
		context['question'] = question
		return render(request,'polls/poll.html', context)
	elif request.method == 'POST':
		data = request.POST
		user = request.user
		obj = Answer.objects.create(user=user, choice_id=data['choice'])
		if obj:
			return HttpResponse("Your vote is done successfully!")
		else:
			return HttpResponse("Error!")

# def poll_edit(request):
