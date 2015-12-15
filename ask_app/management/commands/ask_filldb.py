from django.core.management.base import NoArgsCommand
from ask_app.forms import *
from ask_app.models import *
from random import randint

TAG_AMT = 10000
USR_AMT = 10000
QUE_AMT = 100000
ANS_AMT = 1000000
QVT_AMT = 1000000
AVT_AMT = 2000000

class Command(NoArgsCommand):
	help = "One time run command to fill database with 10k tags, 10k users, 100k questions, 1M answers and 2M votes...\n\nUser password is 123, by the way."
	
	def handle_noargs(self, **options):
		print "~~~Adding 10 000 tags~~~"
		self.add10ktags()
		print "~~~Adding 10 000 users~~~"
		self.add10kusers()
		print "~~~Adding 100 000 qusetions~~~"
		self.add100kquestions()
		print "~~~Adding 1 000 000 answers~~~"
		self.add1Manswers()
		rint "~~~Adding 3 000 000 votes~~~"
		self.add3Mvotes()
		#print "~~~Applying fixes~~~"
		#self.addFix()
		print "~~~Updating ratings~~~"
		self.updateRatings()
		print "~~~Done!~~~"
		
	def add10ktags(self):
		for i in range (1, TAG_AMT + 1):
			name = "Tag_" + `i`
			tag = Tag(tagName=name)
			tag.save()
			
			if i % 1000 == 0: # Every 1000th tag
				print "Added " + `i` + " tag"
	
	def add10kusers(self):
		for i in range (1, USR_AMT + 1):
			login = "User_" + `i`
			email = "user_" + `i` + "@users.com"
			nickname = "User " + `i`
			password = "123"
	
			user = User.objects.create_user(username=login, email=email, password=password)
			extuser = ExtendedAskUser(user = user, nickname = nickname)
			extuser.save()
			
			if i % 1000 == 0: # Every 1000th user
				print "Added " + `i` + " user"
	
	def add100kquestions(self):
		tag_amount = Tag.objects.all().count()
		user_amount = ExtendedAskUser.objects.all().count()
		for i in range (1, QUE_AMT + 1):
			user_number = randint(1, user_amount)
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
			
			title = "Question number " + `i`
			text = "Question number "+`i`+".\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
			
			question = Question(author = user, title = title, text = text)
			question.save()
			question.tags.add(*tags)
			
			if i % 1000 == 0: # Every 1000th question
				print "Added " + `i` + " question"
			
	def add1Manswers(self):
		question_amount = Question.objects.all().count()
		user_amount = ExtendedAskUser.objects.all().count()
		for i in range (1, ANS_AMT + 1):
			user_number = randint(2, user_amount)
			user = User.objects.get(pk=user_number)
		
			question_number = randint(1, question_amount)
			question = Question.objects.get(pk=question_number)
					
			text = "Answer number "+`i`+".\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
			
			answer = Answer(author = user, text = text, question = question)
			answer.save()
			
			if i % 10000 == 0: # Every 10 000th answer
				print "Added " + `i` + " answer"
				
	def add3Mvotes(self):
		question_amount = Question.objects.all().count()
		user_amount = ExtendedAskUser.objects.all().count()
		answer_amount = Answer.objects.all().count()
		for i in range (1, QVT_AMT + 1):
			user_number = randint(2, user_amount)
			user = User.objects.get(pk=user_number)
		
			question_number = randint(1, question_amount)
			question = Question.objects.get(pk=question_number)
		
			vote_sign = randint(0, 1)
	
			QuestionVote.objects.create(user=user, question=question, isDislike = vote_sign)
			
			if i % 10000 == 0: # Every 10 000th vote
				print "Added " + `i` + " question vote"
		
		for i in range (1, AVT_AMT + 1):
			user_number = randint(2, user_amount)
			user = User.objects.get(pk=user_number)
		
			answer_number = randint(1, answer_amount)
			answer = Answer.objects.get(pk=answer_number)
		
			vote_sign = randint(0, 1)
			
			AnswerVote.objects.create(user=user, answer=answer, isDislike = vote_sign)
			
			if i % 10000 == 0: # Every 10 000th vote
				print "Added " + `i` + " answer vote"
								
	def updateRatings(self):
		question_amount = Question.objects.all().count()
		user_amount = ExtendedAskUser.objects.all().count()
		answer_amount = Answer.objects.all().count()
		tag_amount = Tag.objects.all().count()
		
		for i in range (1, question_amount):
			question = Question.objects.get(pk=i)
			positive_votes = question.votes.filter(questionvote__isDislike=False).count()
			negative_votes = question.votes.filter(questionvote__isDislike=True).count()
			question.rating = positive_votes - negative_votes
			
			answers = question.answer_set.count()
			question.answers_amount = answers
			
			question.save()
			
			if i % 1000 == 0: # Every 1000th question
				print "Updated " + `i` + " question rating"
			
		for i in range (1, answer_amount):
			answer = Answer.objects.get(pk=i)
			positive_votes = answer.votes.filter(answervote__isDislike=False).count()
			negative_votes = answer.votes.filter(answervote__isDislike=True).count()
			answer.rating = positive_votes - negative_votes
			answer.save()
			
			if i % 10000 == 0: # Every 10 000th answer
				print "Updated " + `i` + " answer rating"
			
		for i in range(1, tag_amount):
			tag = Tag.objects.get(pk=i)
			tag_questions = tag.question_set.all()
			rating = 0
			for question in tag_questions:
				rating += question.rating
			
			tag.rating = rating
			tag.save()
			
			if i % 1000 == 0: # Every 1000th tag
				print "Updated " + `i` + " tag rating"
			
		for i in range(1, user_amount):
			user = User.objects.get(pk=i)
			user_questions = user.question_set.all()
			user_answers = user.answer_set.all()
			qrating = 0
			arating = 0
			for question in user_questions:
				qrating += question.rating
			for answer in user_answers:
				arating += answer.rating
			eauser = ExtendedAskUser.objects.get(user=user)
			eauser.rating = qrating + arating
			eauser.save()
			
			if i % 1000 == 0: # Every 1000th user
				print "Updated " + `i` + " user rating"
			
			
# After 2 days python ran out of memory on ~710000 answer vote. Also question had not [1,3] tags, but [1,2] instead.
# Fixes:


	def addFix(self):
		question_amount = Question.objects.all().count()
		user_amount = ExtendedAskUser.objects.all().count()
		answer_amount = Answer.objects.all().count()
		tag_amount = Tag.objects.all().count()
		
		for i in range(1, question_amount):
			question = Question.objects.get(pk=i)
			tags = question.tags
			tag_number_list = []
			for j in range(1, tags.count()):
				tag_number = tags.all()[j].pk
				tag_number_list.append(tag_number)
				
			added = False
			tag_id = 1
			while (added != True):
				tag_id = randint(1,tag_amount)
				if not tag_id in tag_number_list:
					added = True
			newtag = []
			tag = Tag.objects.get(pk=tag_id)
			newtag.append(tag)
			question.tags.add(*newtag)
			
			if i % 1000 == 0: # Every 1000th question
				print "Added one tag to " + `i` + " question"
		
		
		# Additional million of answervotes.
		for i in range (1, 1000001):
			user_number = randint(2, user_amount)
			user = User.objects.get(pk=user_number)
		
			answer_number = randint(1, answer_amount)
			answer = Answer.objects.get(pk=answer_number)
		
			vote_sign = randint(0, 1)
			
			AnswerVote.objects.create(user=user, answer=answer, isDislike = vote_sign)
			
			if i % 10000 == 0: # Every 10 000th vote
				print "Added " + `i` + " answer vote"
			