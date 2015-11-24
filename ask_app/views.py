from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from ask_app.models import *

# Create your views here.

from logic import *
#from forms import *

# Done
def main_page(request):
	question_list = Question.objects.newest()
	context = {}
	tql = paginate(question_list, 1)
	question_list = Question.objects.form_dictionary(query=tql['questions'].object_list)
	context.update({'title': 'Titled template', 'user': ExtendedAskUser.objects.user_info(user_1=request.user), 'question_list': question_list, 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)
	# TODO: logic
	
# Done
def	hot_questions(request):
	user = temporary_question_list[0]['author']
	context = {}
	tql = paginate(temporary_question_list, 1)	# IRL will be select questions order by rating
	context.update({'title': 'Titled template', 'user': user, 'question_list': tql['questions'], 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)

# Done
def	tag(request, tag_name):
	user = temporary_question_list[0]['author']
	context = {}
	tql = paginate(temporary_question_list * 4, 1)	# IRL will be select tags where name like %
	context.update({'title': 'Titled template', 'user': user, 'question_list': tql['questions'], 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)

# Done
def questions(request, page_num=1):
	user = temporary_question_list[0]['author']
	context = {}
	tql = paginate(temporary_question_list * 4, page_num)
	context.update({'title': 'Titled template', 'user': user, 'question_list': tql['questions'], 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)

# Done
def question(request, question_num):
	try:
		question_answers = Question.objects.one_question_answers(id=question_num)
	except Question.DoesNotExist:
		raise Http404
	context = {}
	context.update({'title': 'Answers to ' + question_answers['question']['title'], 'user': ExtendedAskUser.objects.user_info(user_1=request.user), 'question': question_answers['question'], 'answers': question_answers['answers'], 'right_block': right_block()})
	return render(request, 'question_answers.html', context)

# Done
@login_forbidded
def login(request):
	#if request.POST:
	#	username = request.POST.get('username')
	#	password = request.POST.get('password')
	#	user = auth.authenticate(username=username, password=password)
	#	if user is not None:
	#		return redirect(previous_page)
	#	else
	#		# return json that user data  is  incorrect.
	#		pass
	#else:
		context = {}
		context.update({'title': 'Log in', 'right_block': right_block(), 'previous_page': request.GET.urlencode })
		return render(request, 'login.html', context)

# Done
@login_forbidded
def register(request):
	#if request.POST:
	#	form = UserForm(request.POST)
	#	if form.is_valid():
	#		username = form.cleaned_data.get('username')
	#		user = contrib.auth.models.User.objects.create_user(username, ...)
	#		user.save()
	#	# should be like
	#	# if form.is_valid():
	#	#	form.save()
	#	## or better if save_form_if_valid():
	#	## redicert('/')
	#	## else error.
	#else:
	#	form = UserForm(request.POST)
		context = {}
		context.update({'title': 'Register', 'right_block': right_block(), 'form': UserForm()})
		return render(request, 'register.html', context)

# Done
@login_required
def ask(request):
	user = temporary_question_list[0]['author']
	context = {}
	context.update({'title': 'Ask your question', 'user': user, 'right_block': right_block()})
	return render(request, 'ask.html', context)

# Done
@login_required
def settings(request):
	user = temporary_question_list[0]['author']
	context = {}
	context.update({'title': 'Settings', 'user': user, 'right_block': right_block()})
	return render(request, 'settings.html', context)

# WIP
@login_required
def logout(request):
	# Kinda user->logout, then redirect to main page.
	return HttpResponseRedirect("/")

# WIP. And probably never will be ready...
def search(request, search_string):
	user = temporary_question_list[0]['author']
	context = {}
	context.update({'title': 'Searching for' + search_string, 'search_string': search_string, 'user': user, 'right_block': right_block()})
	return render(request, 'search.html', context)