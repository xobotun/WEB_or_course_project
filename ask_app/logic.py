import random
from django.core.paginator import Paginator

temporary_question_list = [
	{ 'id': 1, 'author': {'name': 'User 1', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 1}, 'rating': 5, 'title': 'My First Question', 'text': 'This is text. Python, please multiply it a few times!', 'tags': {'tag1name': 'Alpha', 'tag2name':'and', 'tag3name':'Omega'}, 'comments_amount': 42 },
	{ 'id': 2, 'author': {'name': 'User 2', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 2}, 'rating': 0, 'title': 'Test', 'text': 'Testing test toster.', 'tags': {'tag1name':'test'}, 'comments_amount': 0 },
	{ 'id': 3, 'author': {'name': 'Author', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 999}, 'rating': 9, 'title': 'Ode', 'text': 'Ode to my laziness!..', 'tags': {'tag1name':'I\'m lazy'}, 'comments_amount': 1 },
	{ 'id': 4, 'author': {'name': 'User 4', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 3}, 'rating': -1, 'title': 'HELP ME!!!! URGENt!!!1', 'text': 'wheres ussr niumer 3??????', 'tags': {'tag1name':'HALP!!'}, 'comments_amount': 132 },
	{ 'id': 5, 'author': {'name': 'User 5', 'userpic_path': 'http://lorempixel.com/100/100', 'id': 4}, 'rating': 0, 'title': 'My First Question', 'text': 'This is text.', 'tags': {'tag1name': 'Alpha', 'tag2name':'and', 'tag3name':'Omega'}, 'comments_amount': 2 },

	]

temporary_tag_list = [
	{'name': 'Alpha', 'value': '10'},
	{'name': 'And', 'value': '5'},
	{'name': 'Omega', 'value': '0'},
]

def one_question_for_question_page(number = 0):
	if (number == 0):
		number = random.randint(0,3)
	return temporary_question_list[number - 1]
	
def paginate(objects, number):
	paginator = Paginator(objects, 4, 1)	# By 4 questions on page, allowing 1 orphan
	try:
		page = paginator.page(number)
	except EmptyPage:
		page = paginator.page(1)
	return {'current_page': number,
			'questions': page, 
			'has_previous': page.has_previous(), 
			'has_next': page.has_next(), 
			'previous_number': int(number) - 1, 
			'next_number': int(number) + 1}
	
def right_block():
	temp_user_list = []
	for i in range(0,3):
		temp_user_list += temporary_question_list[i]['author']
	return {'tags': temporary_tag_list, 'users': temp_user_list}