from django.core.management.base import BaseCommand
from ask_app.forms import *
from ask_app.models import *
from random import randint

class Command(BaseCommand):
	help = "One time run command to fill database with 10k tags, 10k users, 100k questions, 1M answers and 2M votes...\n\nUser password is 123, by the way."
	
	def handle_noargs(self, **options):
		self.add10ktags()
		self.add10kusers()
		self.add100kquestions()
		self.add1Manswers()
		self.add3Mvotes()
		slef.updateRatings()
		
	def add10ktags(self):
		for i in range (1, 10000):
			name = "Tag_" + `i`
			tag = Tag(tagName=name)
			tag.save()
	
	def add10kusers(self):
		for i in range (1, 10000):
			login = "User_" + `i`
			email = "user_" + `i` + "@users.com"
			nickname = "User " + `i`
			password = "123"
	
			user = User.objects.create_user(username=login, email=email, password=password)
			extuser = ExtendedAskUser(user = user, nickname = nickname)
			extuser.save()
	
	def add100kquestions(self):
		tag_amount = Tag.objects.all().count()
		user_amount = ExtendedAskUser.objects.all().count()
		for i in range (1, 100000):
			user_number = randint(1, user_amount) # Except root user №1.
			user = User.objects.get(pk=user_number)
			
			tags_amount = randint(1,3)
			tag_number_list=[]
			while (len(tag_number_list) != tags_amount):
				tag_id = randint(1,tag_amount)
				if not tag_id in tag_number_list:
					tag_number_list.append(tag_id)
			tags = []
			for j in range(1, tags_amount):
				tag = Tag.objects.get(pk=tag_number_list[j-1])
				tags.append(tag)
			
			title = "Question №" + `i`
			text = "Question №"+`i`+".\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
			
			question = Question(author = user, title = title, text = text)
			question.save()
			question.tags.add(*tags)
			
	def add1Manswers(self):
		question_amount = Question.objects.all().count()
		user_amount = ExtendedAskUser.objects.all().count()
		for i in range (1, 1000000):
			user_number = randint(2, user_amount) # Except root user №1.
			user = User.objects.get(pk=user_number)
		
			question_number = randint(1, question_amount)
			question = Question.objects.get(pk=question_number)
					
			text = "Answer №"+`i`+".\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
			
			answer = Answer(author = user, text = text, question = question)
			answer.save()
				
	def add3Mvotes(self):
		question_amount = Question.objects.all().count()
		user_amount = ExtendedAskUser.objects.all().count()
		answer_amount = Answer.object.all().count()
		for i in range (1, 1000000):
			user_number = randint(2, user_amount) # Except root user №1.
			user = User.objects.get(pk=user_number)
		
			question_number = randint(1, question_amount)
			question = Question.objects.get(pk=question_number)
		
			vote_sign = randint(0, 1) # 0 == Like, 1 == Dislike
	
			QuestionVote.objects.create(user=user, question=question, isDislike = vote_sign)
		
		for i in range (1, 2000000):
			user_number = randint(2, user_amount) # Except root user №1.
			user = User.objects.get(pk=user_number)
		
			answer_number = randint(1, answer_amount)
			answer = Answer.objects.get(pk=answer_number)
		
			vote_sign = randint(0, 1) # 0 == Like, 1 == Dislike
			
			AnswerVote.objects.create(user=user, answer=answer, isDislike = vote_sign)
				
	def updateRatings(self):
		question_amount = Question.objects.all().count()
		user_amount = ExtendedAskUser.objects.all().count()
		answer_amount = Answer.object.all().count()
		tag_amount = Tag.objects.all().count()
		
		for i in range (1, question_amount):
			question = Question.objects.get(pk=i)
			positive_votes = question.votes.filter(questionvote__isDislike=False).count()
			negative_votes = question.votes.filter(questionvote__isDislike=True).count()
			question.rating = positive_votes - negative_votes
			
			answers = question.answer_set.count()
			question.answers_amount = answers
			
			question.save()
			
		for i in range (1, answer_amount):
			answer = Answer.objects.get(pk=i)
			positive_votes = answer.votes.filter(answervote__isDislike=False).count()
			negative_votes = answer.votes.filter(answervote__isDislike=True).count()
			answer.rating = positive_votes - negative_votes
			answer.save()
			
		for i in range(1, tag_amount):
			tag = Tag.objects.get(pk=i)
			tag_questions = tag.question_set
			rating = 0
			for question in tag_questions:
				rating += question.rating
			
			tag.rating = rating
			tag.save()
			
		for i in range(1, user_amount):
			user = User.objects.get(pk=i)
			user_questions = user.question_set
			user_answers = user.answer_set
			qrating = 0
			arating = 0
			for question in user_questions:
				qrating += question.rating
			for answer in user_answers:
				arating += answer.rating
			eauser = ExtendedAskUser.get(user=user)
			eauser.rating = qrating + arating
			eauser.save()
			
			