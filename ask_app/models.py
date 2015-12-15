from django.db import models
from django.contrib.auth.models import User, AnonymousUser # generic user
from django.utils import timezone	# Make every occurency to datetime.
#from ask_app.logic import *

###
##	Managers
###

class ExtendedUserManager(models.Manager):
	
	def popular(self):
		return self.order_by('-rating')
		
	def top10(self):
		return self.exclude(user=1).order_by('-rating')[:10]
		
	def form_dictionary(self, user_1):
		if (bool(user_1.userpic) == False):
			userpic = self.get(nickname="DEBUG USER").userpic
		else:
			userpic = user_1.userpic
		return {'name': user_1.nickname, 'userpic_path': userpic.url, 'id': user_1.user.pk, 'rating': user_1.rating, 'is_authenticated': True}
	
	def user_info(self, user_1):
		if (type(user_1) == AnonymousUser):
			return None
		ext_user = self.get(user=user_1)
		return self.form_dictionary(user_1=ext_user)
		
	def create_user(self, user_login, user_password, user_email, user_nickname, user_pic):
		user = User.objects.create_user(user_login, user_email, user_password)
		extuser = ExtendedAskUser(user=user, nickname=user_nickname, userpic=user_pic)
		return extuser.save()
		
#	def attempt_to_vote(self, ea_user, data):
#		if ea_user == None:
#			return ajax_dict(type='error', message='You need to be logged in to do that!')
#		else:
#			if data.get('type') == 'question_vote': # Should it be a seperate function?
#				quid = 0
#				vote_isDislike = False
#				try:
#					quid = int(data.get('message').get('question_id'))
#				except ValueError:
#					return erroneous_ajax_dict()
#				if data.get('message').get('vote_sign') == 'up':
#					vote_isDislike = False
#				elif data.get('message').get('vote_sign') != 'down':
#					vote_isDislike = True
#				else:
#					return erroneous_ajax_dict()
#				return QuestionManager.vote(user=ea_user.user, id=quid, sign=vote_isDislike)
#			elif data.get('type') == 'answer_vote': # Should it be a seperate function?
#				quid = 0
#				aid = 0
#				vote_isDislike = False
#				try:
#					quid = int(data.get('message').get('question_id'))
#					aid = int(data.get('message').get('answer_id'))
#				except ValueError:
#					return erroneous_ajax_dict()
#				if data.get('message').get('vote_sign') == 'up':
#					vote_isDislike = False
#				elif data.get('message').get('vote_sign') != 'down':
#					vote_isDislike = True
#				else:
#					return erroneous_ajax_dict()
#				return AnswerManager.vote(user=ea_user.user, id=quid, sign=vote_isDislike)
				

class QuestionManager(models.Manager):
	
	def newest(self):
		return self.order_by('-rating')
		
	def oldest(self):
		return self.order_by('created')
		
	def hot(self):
		return self.order_by('-rating')
		
	def nonhot(self):
		return self.order_by('rating')
		
	def one_question(self, question):
		author_dict = ExtendedAskUser.objects.user_info(user_1=question.author)
		tags_list = Tag.objects.form_dictionary(question.tags.all())
		question_dict = { 'id': question.pk, 'author': author_dict, 'rating': question.rating, 'title': question.title, 'text': question.text, 'tags': tags_list, 'comments_amount': question.answers_amount, 'created': question.created }
		return question_dict
		
	def one_question_answers(self, id):
		question = self.get(pk=id)
		question_answers_dict = {'question': self.one_question(question=question), 'answers': Answer.objects.best(query=question.answer_set.all())}
		return question_answers_dict
		
	def form_dictionary(self, query):
		questions_list = []
		for question in query:
			questions_list.append(self.one_question(question=question))
		return questions_list
		
	def increase_answers_counter(self, id):
		question = self.get(pk=id)
		question.answers_amount += 1
		question.save()
		
#	def vote(self, user, id, sign):
#		#qtype = 'error'
#		#qmessage = 'Sum Thung Wong'
#		qtype = 'success'
#		qmessage = 'You have succesfully voted!'
#		question = self.get(pk=id)
#		if sign:
#			rating_delta = 1 
#		else:
#			rating_delta = -1
#		try:
#			user_vote = question.questionvote_set.filter(user__exact=user)[0]
#			if user_vote.isDislike == sign:
#				qtype = 'error'
#				qmessage = 'You have already voted!'
#			if user_vote.isDislike:
#				rating_delta += 1 # -1 If liked, +1 if disliked, 0 if had never voted. Will be added to question.rating
#			else:
#				rating_delta += -1
#			#question.questionvote_set.remove(user_vote)
#			user_vote.delete()
#		except QuestionVote.DoesNotExist:
#			pass
#		qv = QuestionVote.objects.create(user=user, question=question, isDislike = sign)
#		question.questionvote_set.add(qv)
#		question.rating += rating_delta
#		question.save()
#		return ajax_dict(type=qtype, message=qmessage)
		

		
class AnswerManager(models.Manager):
	
	def best(self, query):
		#answer_query = query.order_by('-rating').order_by('-isBestAnswer')
		answer_query_part1 = query.filter(isBestAnswer__exact=True).order_by('-rating')
		answer_query_part2 = query.filter(isBestAnswer__exact=False).order_by('-rating')
		final_dict = self.form_dictionary(query=answer_query_part1) + self.form_dictionary(query=answer_query_part2)
		return final_dict
		
	def form_dictionary(self, query):
		answers_list = []
		for answer in query:
			answers_list.append(self.one_answer(answer=answer))
		return answers_list
		
	def one_answer(self, answer):
		author_dict = ExtendedAskUser.objects.user_info(user_1=answer.author)
		answer_dict = { 'id': answer.pk, 'author': author_dict, 'rating': answer.rating, 'text': answer.text, 'created': answer.created, 'isBestAnswer': answer.isBestAnswer }
		return answer_dict
		
#	def vote(self, user, id, sign):
#		#qtype = 'error'
#		#qmessage = 'Sum Thung Wong'
#		atype = 'success'
#		amessage = 'You have succesfully voted!'
#		answer = self.get(pk=id)
#		if sign:
#			rating_delta = 1 
#		else:
#			rating_delta = -1
#		try:
#			user_vote = answer.answervote_set.filter(user__exact=user)[0]
#			if user_vote.isDislike == sign:
#				atype = 'error'
#				amessage = 'You have already voted!'
#			if user_vote.isDislike:
#				rating_delta += 1 # -1 If liked, +1 if disliked, 0 if had never voted. Will be added to question.rating
#			else:
#				rating_delta += -1
#			#question.questionvote_set.remove(user_vote)
#			user_vote.delete()
#		except AnswerVote.DoesNotExist:
#			pass
#		av = AnswerVote.objects.create(user=user, answer=answer, isDislike = sign)
#		answer.answervote_set.add(av)
#		answer.rating += rating_delta
#		answer.save()
#		return ajax_dict(type=atype, message=amessage)
		
class TagManager(models.Manager):
	
	def best(self):
		return self.order_by('-rating')[:20]
		
	def one_tag(self, tag):
		return {'name': tag.tagName, 'rating': tag.rating}
		
	def form_dictionary(self, query):
		tags_list = []
		for tag in query:
			tags_list.append(self.one_tag(tag=tag))
		return tags_list
		
		
###
##	Models
###
		
def userpic_upload_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>_<filename>
	return 'user_{0}_{1}'.format(instance.user.id, filename)

class ExtendedAskUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
	# Already existing:
	#	login    aka username
	#	password aka password
	#	email    aka email
	#	id       aka pk
	nickname = models.CharField(max_length=30, unique=True)	# Standart Django limitation is 30 characters too.
	userpic = models.FileField(upload_to=userpic_upload_path, blank=True)
	rating = models.IntegerField(default=0, db_index=True)
	
	objects = ExtendedUserManager()
	
	def __unicode__(self):
		return self.nickname
		
	class Meta:
		ordering = ['rating']
		
		
class Question(models.Model):
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255)
	text = models.TextField()
	rating = models.IntegerField(default=0, db_index=True)
	votes = models.ManyToManyField(User, through = 'QuestionVote', related_name="QuestionVotes", related_query_name="QuestionVote")
	created = models.DateTimeField(default=timezone.now, db_index=True)
	tags = models.ManyToManyField('Tag')
	answers_amount = models.PositiveIntegerField(default=0)
	
	objects = QuestionManager()

	def __unicode__(self):
		return self.title + "\n" + self.text
		
	class Meta:
		ordering = ['-pk']
		
		
class Answer(models.Model):
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # generic user, create my own user, _basing on this one_!
	text = models.TextField()
	rating = models.IntegerField(default=0, db_index=True)
	votes = models.ManyToManyField(User, through = 'AnswerVote', related_name="AnswerVotes", related_query_name="AnswerVote")	# Cascade delete should delete only related votes. What about rating integrity?
	created = models.DateTimeField(default=timezone.now)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	isBestAnswer = models.BooleanField(default=False, db_index=True)
	
	objects = AnswerManager()
	
	def __unicode__(self):
		return self.text
		
	class Meta:
		ordering = ['-rating']
		

class QuestionVote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	isDislike = models.BooleanField(default='False')
	
	def __unicode__(self):
		if self.isDislike:
			way = "down"
		else:
			way = "up"
		return self.user + " voted " + way + " question " + question.id
	
	
class AnswerVote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	isDislike = models.BooleanField(default='False')
	
	def __unicode__(self):
		if self.isDislike:
			way = "down"
		else:
			way = "up"
		return self.user + " voted " + way + " answer " + answer.id
	
	
class Tag(models.Model):
	tagName = models.CharField(max_length=255, unique=True)
	rating = models.IntegerField(default=0, db_index=True)
	
	objects = TagManager()
	
	def __unicode__(self):
		return self.tagName
		
	class Meta:
		ordering = ['rating']