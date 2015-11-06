import random

temporary_question_list = [
	{ 'id': 1, 'author': 'User 1', 'rating': 5, 'title': 'My First Question', 'text': 'This is text. Python, please multiply it a few times!', 'tags': ['Alpha', 'and', 'Omega'], 'comments_amount': 42 },
	{ 'id': 2, 'author': 'User 2', 'rating': 0, 'title': 'Test', 'text': 'Testing test toster.', 'tags': ['test'], 'comments_amount': 0 },
	{ 'id': 3, 'author': 'Author', 'rating': 9, 'title': 'Ode', 'text': 'Ode to my laziness!..', 'tags': ['I\'m lazy'], 'comments_amount': 1 },
	{ 'id': 4, 'author': 'User 4', 'rating': -1, 'title': 'HELP ME!!!! URGENt!!!1', 'text': 'wheres ussr niumer 3??????', 'tags': ['HALP!!'], 'comments_amount': 132 },
]

def one_question_for_question_page(number = 0):
	if (number == 0):
		number = random.randint(0,3)
	return temporary_question_list[number]