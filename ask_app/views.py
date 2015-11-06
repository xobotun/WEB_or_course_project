from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

from logic import *

def main_page(request):
	# user = one_question_for_question_page(0);
	user = temporary_question_list[0]['author']
	context = {}
	context.update({'title': 'Titled template', 'user': user, 'question_list': temporary_question_list, 'paginator': paginator})
	return render(request, 'main_page.html', context)
	# TODO: logic
	
def	hot_questions(request):
	return HttpResponseRedirect("/")

def	tag(request, tag_name):
	return HttpResponseRedirect("/")

def questions(request, page_num):
	return HttpResponseRedirect("/")

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