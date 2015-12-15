import random
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, AnonymousUser # generic user
from ask_app.models import *
	
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
	
def get_user_dict(request):
	#if ((request.user) == AnonymousUser):
	if (request.user.is_authenticated()):
		return ExtendedAskUser.objects.user_info(user_1=request.user)
	#if ((request.user) == User):
	else:
		return None

def get_user(request):
	if (request.user.is_authenticated()):
		return ExtendedAskUser.objects.get(user=request.user)
	else:
		return None
		
def right_block():
	top_users_query = ExtendedAskUser.objects.top10()
	top_users_list = []
	for user in top_users_query:
		top_users_list.append(ExtendedAskUser.objects.form_dictionary(user))
	top_tags_list = Tag.objects.form_dictionary(Tag.objects.best())
	return {'tags': top_tags_list, 'users': top_users_list}
	
def ajax_dict(type, message):
	return {'type': type, 'message': message}
	
def erroneous_ajax_dict():
	return ajax_dict(type='None', message='Something went wrong!')
	
def set_previous_page(request):
	request.session['previous_page'] = request.META.get('PATH_INFO')
	
def get_previous_page(request):
	try:
		pre_page = request.session['previous_page']
		del request.session['previous_page']
	except KeyError:
		return '/'
	return pre_page