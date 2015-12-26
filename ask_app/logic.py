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
	
def attempt_to_vote(ea_user, data):
		if ea_user == None:
			return ajax_dict(type='error', message='You need to be logged in to do that!')
		else:
			if data.get('type') == 'question_vote': # Should it be a seperate function?
				quid = 0
				vote_isDislike = False
				try:
					quid = int(data.get('message[question_id]'))
				except ValueError:
					return erroneous_ajax_dict()
				if data.get('message[vote_sign]') == 'up':
					vote_isDislike = False
				elif data.get('message[vote_sign]') == 'down':
					vote_isDislike = True
				else:
					return erroneous_ajax_dict()
				return question_vote(user=ea_user.user, id=quid, sign=vote_isDislike)
			elif data.get('type') == 'answer_vote': # Should it be a seperate function?
				quid = 0
				aid = 0
				vote_isDislike = False
				try:
					quid = int(data.get('message[question_id]'))
					aid = int(data.get('message[answer_id]'))
				except ValueError:
					return erroneous_ajax_dict()
				if data.get('message[vote_sign]') == 'up':
					vote_isDislike = False
				elif data.get('message[vote_sign]') == 'down':
					vote_isDislike = True
				else:
					return erroneous_ajax_dict()
				return answer_vote(user=ea_user.user, id=aid, sign=vote_isDislike)

				
def attempt_to_checkbox(ea_user, data):
	quid = int(data.get('message[question_id]'))
	question = Question.objects.get(pk=quid)
	if ea_user == None:
		return ajax_dict(type='error', message='You need to be logged in to do that!')
	elif ea_user.user != question.author:
		return ajax_dict(type='error', message='You can not vote for answer not related to your question!')
	else:
		aid = 0
		try:
			aid = int(data.get('message[answer_id]'))
		except ValueError:
			return erroneous_ajax_dict()
		atype = 'success'
		amessage = 'You have succesfully marked this answer as useful!'
		answer = Answer.objects.get(pk=aid)
		answer.isBestAnswer = not answer.isBestAnswer
		answer.save()
		aiba = False
		if (answer.isBestAnswer == True):
			aiba = True
		return ajax_dict(type=atype, message={'text': amessage, 'new_state': aiba, 'answer_id': aid})
		
def question_vote(user, id, sign):
	#qtype = 'error'
	#qmessage = 'Sum Thung Wong'
	qtype = 'success'
	qmessage = 'You have succesfully voted!'
	question = Question.objects.get(pk=id)
	if sign:
		rating_delta = -1 
	else:
		rating_delta = 1
	try:
		user_vote = question.questionvote_set.filter(user__exact=user)[0]
		if user_vote.isDislike == sign:
			qtype = 'error'
			qmessage = 'You have already voted!'
		if user_vote.isDislike:
			rating_delta += 1 # -1 If liked, +1 if disliked, 0 if had never voted. Will be added to question.rating
		else:
			rating_delta += -1
		#question.questionvote_set.remove(user_vote)
		user_vote.delete()
	except IndexError:
		pass
	qv = QuestionVote.objects.create(user=user, question=question, isDislike = sign)
	question.questionvote_set.add(qv)
	question.rating += rating_delta
	question.save()
	return ajax_dict(type=qtype, message={'text': qmessage, 'new_rating': question.rating, 'question_id': id})
	
def answer_vote(user, id, sign):
	#qtype = 'error'
	#qmessage = 'Sum Thung Wong'
	atype = 'success'
	amessage = 'You have succesfully voted!'
	answer = Answer.objects.get(pk=id)
	if sign:
		rating_delta = -1 
	else:
		rating_delta = 1
	try:
		user_vote = answer.answervote_set.filter(user=user)[0]
		if user_vote.isDislike == sign:
			atype = 'error'
			amessage = 'You have already voted!'
		if user_vote.isDislike:
			rating_delta += 1 # -1 If liked, +1 if disliked, 0 if had never voted. Will be added to question.rating
		else:
			rating_delta += -1
		#question.questionvote_set.remove(user_vote)
		user_vote.delete()
	except IndexError:
		pass
	av = AnswerVote.objects.create(user=user, answer=answer, isDislike = sign)
	answer.answervote_set.add(av)
	answer.rating += rating_delta
	answer.save()
	return ajax_dict(type=atype, message={'text': amessage, 'new_rating': answer.rating, 'answer_id': id})