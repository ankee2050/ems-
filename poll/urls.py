from django.urls import path
from .views import *

urlpatterns = [
	path('add/', PollView.as_view(), name='polls_add'),
	path('<int:id>/edit/', PollView.as_view(), name='polls_edit'),
	path('<int:id>/delete/', PollDelete.as_view(), name='polls_delete'),
	path('list/', index, name='polls_list'),
	path('<int:id>/details/', details, name='poll_details'),
	path('<int:id>/', vote_poll, name='poll_vote'),
]