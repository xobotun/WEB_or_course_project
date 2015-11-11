from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

# Create your views here.

from logic import *

# Done
def main_page(request):
	# user = one_question_for_question_page(0);
	user = temporary_question_list[0]['author']
	context = {}
	tql = paginate(temporary_question_list * 4, 1)
	context.update({'title': 'Titled template', 'user': user, 'question_list': tql['questions'], 'paginator': tql, 'right_block': right_block()})
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
	tql = paginate(temporary_question_list * 4, page_num)	# IRL will be select tags where name like %
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
	user = temporary_question_list[0]['author']
	try:
		temporary_question_list[int(question_num)]
	except IndexError:
		raise Http404
	context = {}
	context.update({'title': 'Answers to ' + temporary_question_list[int(question_num)]['title'], 'user': user, 'question': temporary_question_list[int(question_num)], 'answers': temporary_answer_list, 'right_block': right_block()})
	return render(request, 'question_answers.html', context)

# WIP
def login(request):
	return HttpResponseRedirect("/")

# WIP
def register(request):
	return HttpResponseRedirect("/")

# WIP
def ask(request):
	return HttpResponseRedirect("/")

# WIP
def settings(request):
	return HttpResponseRedirect("/")

# WIP
def logout(request):
	return HttpResponseRedirect("/")

# WIP
def search(request):
	return HttpResponseRedirect("/")