from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from ask_app.models import *
from ask_app.forms import *

# Create your views here.

from logic import *
#from forms import *

# Done
def main_page(request):
	question_list = Question.objects.newest()
	context = {}
	tql = paginate(question_list, 1)
	question_list = Question.objects.form_dictionary(query=tql['questions'].object_list)
	context.update({'title': 'Titled template', 'user': get_user(request), 'question_list': question_list, 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)
	
# Done
def	hot_questions(request):
	question_list = Question.objects.hot()
	context = {}
	tql = paginate(question_list, 1)
	question_list = Question.objects.form_dictionary(query=tql['questions'].object_list)
	context.update({'title': 'Titled template', 'user': get_user(request), 'question_list': question_list, 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)

# Done
def	tag(request, tag_name):
	question_list = Question.objects.filter(tags__tagName=tag_name)
	context = {}
	tql = paginate(question_list, 1)
	question_list = Question.objects.form_dictionary(query=tql['questions'].object_list)
	context.update({'title': 'Titled template', 'user': get_user(request), 'question_list': question_list, 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)

# Done
def questions(request, page_num=1):
	question_list = Question.objects.newest()
	if (request.GET.get('sort') == 'date'):
		if (request.GET.get('order') == 'desc'):
			question_list = Question.objects.newest()
		if (request.GET.get('order') == 'asc'):
			question_list = Question.objects.oldest()
	if (request.GET.get('sort') == 'rating'):
		if (request.GET.get('order') == 'desc'):
			question_list = Question.objects.hot()
		if (request.GET.get('order') == 'asc'):
			question_list = Question.objects.nonhot()
	context = {}
	tql = paginate(question_list, page_num)
	question_list = Question.objects.form_dictionary(query=tql['questions'].object_list)
	context.update({'title': 'Titled template', 'user': get_user(request), 'question_list': question_list, 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)

# Done
def question(request, question_num):
	try:
		question_answers = Question.objects.one_question_answers(id=question_num)
	except Question.DoesNotExist:
		raise Http404
	if request.POST:
		form = AnswerForm(request.POST)
		if (form.save(request=request, question_id=question_num)):
			Question.objects.increase_answers_counter(id=question_num)
			return HttpResponseRedirect("/")
		else:
			pass
	else:
		form = AnswerForm()
		user = get_user(request)
		context = {}
		draw_tick = False
		if user is not None:
			if (question_answers['question']['author']['id'] == user['id']):
				draw_tick = True
			
		context.update({'title': 'Answers to ' + question_answers['question']['title'], 'draw_tick': draw_tick, 'form': form, 'user': user, 'question': question_answers['question'], 'answers': question_answers['answers'], 'right_block': right_block()})
		#raise Exception(form)
		return render(request, 'question_answers.html', context)
		#
# Done
def login(request):
	if request.POST:
		form = LoginForm(request.POST)
		if (form.auth_and_login(request=request)):
			return HttpResponseRedirect("/")
		else:
			pass
			raise Exception("Wrong pair")
	else: # if GET
		form = LoginForm()
		context = {}
		context.update({'title': 'Log in', 'right_block': right_block(), 'previous_page': request.GET.urlencode, 'form': form, 'user': get_user(request) })
		return render(request, 'login.html', context)

# Done
def register(request):
	if request.POST:
		form = RegisterForm(request.POST)
		if (form.save(request=request)):
			return HttpResponseRedirect("/")
		else:
			pass
	else:
		form = RegisterForm()
		context = {}
		context.update({'title': 'Register', 'right_block': right_block(), 'previous_page': request.GET.urlencode, 'form': form, 'user': get_user(request) })
		return render(request, 'register.html', context)

# Done
@login_required
def ask(request):
	if request.POST:
		form = QuestionForm(request.POST)
		if (form.save(request=request)):
			return HttpResponseRedirect("/")
		else:
			pass
	else:
		form = QuestionForm()
		context = {}
		context.update({'title': 'Ask your question', 'user': get_user(request), 'right_block': right_block(), 'form': form})
		return render(request, 'ask.html', context)

# Done
@login_required
def settings(request):
	user = temporary_question_list[0]['author']
	context = {}
	context.update({'title': 'Settings', 'user': get_user(request), 'right_block': right_block()})
	return render(request, 'settings.html', context)

# WIP
@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

# WIP. And probably never will be ready...
def search(request, search_string):
	user = temporary_question_list[0]['author']
	context = {}
	context.update({'title': 'Searching for' + search_string, 'search_string': search_string, 'user': user, 'right_block': right_block()})
	return render(request, 'search.html', context)