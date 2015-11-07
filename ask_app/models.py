from django.db import models
from django.contrib.auth.models import User # generic user
import datetime
# Create your models here.

class QuestionManager(models.Manager):
	
	def newest(self):
		return self.order_by('-id')
		
	def hot(self):
		return self.order_by('-rating')

class Question(models.Model):
	author = models.ForeignKey(User) # generic user, create my own user, _basing on this one_!
	title = models.CharField(max_length=255)
	text = models.TextField()
	rating = models.IntegerField(default=0, db_index=True)
	created = models.DateTimeField(default=datetime.datetime.now)
	
	objects = QuestionManager
	#tags = models.ManyToManyField(Tag)
	
	def __unicode__(self):
		return self.title + "\n" + self.text
		
class Answer(models.Model):
	author = models.ForeignKey(User) # generic user, create my own user, _basing on this one_!
	text = models.TextField()
	rating = models.IntegerField()
	created = models.DateTimeField(default=datetime.datetime.now)
	question = models.ForeignKey(Question)
	
	def __unicode__(self):
		return self.text
		
