from django.db import models
from django.contrib.auth.models import User # generic user
from django.utils import timezone	# Make every occurency to datetime.
# Create your models here.

###
##	Managers
###

class ExtendedUserManager(models.Manager):
	
	def popular(self):
		return self.order_by('-rating')
		
	def top10(self):
		return self.order_by('-rating')[10:]


class QuestionManager(models.Manager):
	
	def newest(self):
		return self.order_by('-created')
		
	def oldest(self):
		return self.order_by('created')
		
	def hot(self):
		return self.order_by('-rating')
		
	def nonhot(self):
		return self.order_by('rating')

		
class AnswerManager(models.Manager):
	
	def best(self):
		return self.order_by('-rating').order_by('-isBestAnswer')
		
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
	
	objects = ExtendedUserManager
	
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
	
	objects = QuestionManager

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
	
	objects = AnswerManager
	
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
	
	objects = TagManager
	
	def __unicode__(self):
		return self.tagName
		
	class Meta:
		ordering = ['rating']