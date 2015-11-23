from django.db import models
from django.contrib.auth.models import User # generic user
from django.utils import timezone	# Make every occurency to datetime.

###
##	Managers
###

class ExtendedUserManager(models.Manager):
	
	def popular(self):
		return self.order_by('-rating')
		
	def top10(self):
		return self.order_by('-rating')[:10]
		
	def user_info(self, user_1):
		ext_user = self.get(user=user_1)
		user_dict = {'name': ext_user.nickname, 'userpic_path': ext_user.userpic, 'id': user_1.pk, 'rating': ext_user.rating}

class QuestionManager(models.Manager):
	
	def newest(self):
		question_query = self.order_by('-rating')
		return self.form_dictionary(query=question_query)
		
	def oldest(self):
		return self.order_by('created')
		
	def hot(self):
		return self.order_by('-rating')
		
	def nonhot(self):
		return self.order_by('rating')
		
	def one_question(self, question):
		author_dict = ExtendedAskUser.objects.user_info(user_1=question.author)
		tags_list = []
		tags = question.tags.all()
		for tag in tags:
			tag_dict = {'name': tag.tagName, 'rating': tag.rating}
			tags_list.append(tag_dict)
		question_dict = { 'id': question.pk, 'author': author_dict, 'rating': question.rating, 'title': question.title, 'text': question.text, 'tags': tags_list, 'comments_amount': question.answers_amount, 'created': question.created }
		return question_dict
		
	def one_question_answers(self, id):
		question = self.get(pk=id)
		question_answers_dict = {'question': self.one_question(question=question), 'answers': Answer.objects.form_dictionary(query=question.answers.all())}
		return question_answers_dict
		
	def form_dictionary(self, query):
		questions_list = []
		for question in query:
			questions_list.append(self.one_question(question=question))
		return questions_list

		
class AnswerManager(models.Manager):
	
	def best(self):
		answer_query = self.order_by('-rating').order_by('-isBestAnswer')
		return form_dictionary(query=answer_query)
		
	def form_dictionary(self, query):
		answers_list = []
		for answer in query
			answers_list.append(self.one_answer(answer=answer))
		return answers_list
		
	def one_answer(self, answer):
		author_dict = ExtendedAskUser.objects.user_info(user_1=answer.author)
		answer_dict = { 'id': answer.pk, 'author': author_dict, 'rating': answer.rating, 'text': answer.text, 'created': answer.created, 'isBestAnswer': answer.isBestAnswer }
		return answer_dict
		
class TagManager(models.Manager):
	
	def best(self):
		return self.order_by('-rating')
		
		
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
		ordering = ['rating']
		

class QuestionVote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	isDislike = models.BooleanField(default='False')
	
	
class AnswerVote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	isDislike = models.BooleanField(default='False')
	
	
class Tag(models.Model):
	tagName = models.CharField(max_length=255, unique=True)
	rating = models.IntegerField(default=0, db_index=True)
	
	objects = TagManager()
	
	def __unicode__(self):
		return self.tagName
		
	class Meta:
		ordering = ['rating']