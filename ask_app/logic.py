import random

temporary_question_list = [
	{ 'id': 1, 'author': {'name': 'User 1', 'userpic_path': 'http://lorempixel.org/100/100', 'id': 1}, 'rating': 5, 'title': 'My First Question', 'text': 'This is text. Python, please multiply it a few times!', 'tags': {'tag1name': 'Alpha', 'tag2name':'and', 'tag3name':'Omega'}, 'comments_amount': 42 },
	{ 'id': 2, 'author': {'name': 'User 2', 'userpic_path': 'http://lorempixel.org/100/100', 'id': 2}, 'rating': 0, 'title': 'Test', 'text': 'Testing test toster.', 'tags': {'tag1name':'test'}, 'comments_amount': 0 },
	{ 'id': 3, 'author': {'name': 'Author', 'userpic_path': 'http://lorempixel.org/100/100', 'id': 999}, 'rating': 9, 'title': 'Ode', 'text': 'Ode to my laziness!..', 'tags': {'tag1name':'I\'m lazy'}, 'comments_amount': 1 },
	{ 'id': 4, 'author': {'name': 'User 1', 'userpic_path': 'http://lorempixel.org/100/100', 'id': 3}, 'rating': -1, 'title': 'HELP ME!!!! URGENt!!!1', 'text': 'wheres ussr niumer 3??????', 'tags': {'tag1name':'HALP!!'}, 'comments_amount': 132 },
]

def one_question_for_question_page(number = 0):
	if (number == 0):
		number = random.randint(0,3)
	return temporary_question_list[number - 1]
	
def paginator():
	return {'page': 42}