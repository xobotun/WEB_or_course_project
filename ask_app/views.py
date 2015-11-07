from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

from logic import *

def main_page(request):
	# user = one_question_for_question_page(0);
	user = temporary_question_list[0]['author']
	context = {}
	tql = paginate(temporary_question_list * 4, 1)
	context.update({'title': 'Titled template', 'user': user, 'question_list': tql['questions'], 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)
	# TODO: logic
	
def	hot_questions(request):
	user = temporary_question_list[0]['author']
	context = {}
	tql = paginate(temporary_question_list, 1)	# IRL will be select questions order by rating
	context.update({'title': 'Titled template', 'user': user, 'question_list': tql['questions'], 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)

def	tag(request, tag_name):
	user = temporary_question_list[0]['author']
	context = {}
	tql = paginate(temporary_question_list * 4, page_num)	# IRL will be select tags where name like %
	context.update({'title': 'Titled template', 'user': user, 'question_list': tql['questions'], 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)

def questions(request, page_num=1):
	user = temporary_question_list[0]['author']
	context = {}
	tql = paginate(temporary_question_list * 4, page_num)
	context.update({'title': 'Titled template', 'user': user, 'question_list': tql['questions'], 'paginator': tql, 'right_block': right_block()})
	return render(request, 'main_page.html', context)

def question(request, question_num):
	return HttpResponseRedirect("/")

def login(request):
	return HttpResponseRedirect("/")

def register(request):
	return HttpResponseRedirect("/")

def ask(request):
	return HttpResponseRedirect("/")

def settings(request):
	return HttpResponseRedirect("/")

def logout(request):
	return HttpResponseRedirect("/")
	
def search(request):
	return HttpResponseRedirect("/")