import random
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, AnonymousUser # generic user
from ask_app.models import *

temporary_question_list = [
	{ 'id': 1, 'author': {'name': 'User 1', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 1}, 'rating': 5, 'title': 'My First Question', 'text': 'This is text. Python, please multiply it a few times!', 'tags': {'Alpha', 'and', 'Omega'}, 'comments_amount': 42 },
	{ 'id': 2, 'author': {'name': 'User 2', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 2}, 'rating': 0, 'title': 'Test', 'text': 'Testing test toster.', 'tags': {'test'}, 'comments_amount': 0 },
	{ 'id': 3, 'author': {'name': 'Author', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 999}, 'rating': 9, 'title': 'Ode', 'text': 'Ode to my laziness!..', 'tags': {'BakaWrongTag'}, 'comments_amount': 1 },
	{ 'id': 4, 'author': {'name': 'User 4', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 3}, 'rating': -1, 'title': 'HELP ME!!!! URGENt!!!1', 'text': 'wheres ussr niumer 3??????', 'tags': {'HALP111'}, 'comments_amount': 132 },
	{ 'id': 5, 'author': {'name': 'User 5', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 4}, 'rating': 0, 'title': 'My First Question', 'text': 'This is text.', 'tags': {'Alpha', 'and', 'Omega'}, 'comments_amount': 2 },

	]

temporary_tag_list = [
	{'name': 'Alpha', 'value': '10'},
	{'name': 'And', 'value': '5'},
	{'name': 'Omega', 'value': '0'},
]

temporary_answer_list = [
	{ 'id': 1, 'author': {'name': 'User 1', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 1}, 'rating': 5, 'parent': 1, 'text': 'This is text. Python, please multiply it a few times!'},
	{ 'id': 2, 'author': {'name': 'User 2', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 2}, 'rating': 0, 'parent': 1, 'text': 'Testing test toster.'},
	{ 'id': 3, 'author': {'name': 'Author', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 999}, 'rating': 9, 'parent': 1, 'text': 'Ode to my laziness!..'},
	{ 'id': 4, 'author': {'name': 'User 4', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 3}, 'rating': -1, 'parent': 1, 'text': 'wheres ussr niumer 3??????'},
	{ 'id': 5, 'author': {'name': 'User 5', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 4}, 'rating': 0, 'parent': 1, 'text': 'This is text.'},

	]

def one_question_for_question_page(number = 0):
	if (number == 0):
		number = random.randint(0,3)
	return temporary_question_list[number - 1]
	
def paginate(objects, number):
	paginator = Paginator(objects, 4, 1)	# By 4 questions on page, allowing 1 orphan
	try:
		page_num = paginator.page(number)
	except EmptyPage:
		#page = paginator.page(1)
		raise Http404
	
	pages = paginator.page_range
	pages_around_current = []
	number_size = 3
	for page_number in pages:
		if (page_number >= int(number) - number_size and page_number <= int(number) + number_size):
			pages_around_current.append(page_number)
		
	return {'current_page': number,
			'questions': page_num, 
			'has_previous': page_num.has_previous(), 
			'has_next': page_num.has_next(), 
			'previous_number': int(number) - 1, 
			'next_number': int(number) + 1,
			'other_pages': pages_around_current,
			'first_page': pages[0],
			'last_page': pages[-1],
			}
	
def get_user(request):
	#if ((request.user) == AnonymousUser):
	if (request.user.is_authenticated):
		return ExtendedAskUser.objects.user_info(user_1=request.user)
	#if ((request.user) == User):
	else:
		return None
		

def right_block():
	top_users_query = ExtendedAskUser.objects.top10()
	top_users_list = []
	for user in top_users_query:
		top_users_list.append(ExtendedAskUser.objects.form_dictionary(user))
	top_tags_list = Tag.objects.form_dictionary(Tag.objects.best())
	return {'tags': top_tags_list, 'users': top_users_list}