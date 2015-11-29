from ask_app.models import *
from django.contrib.auth.models import User, AnonymousUser
from django import forms
from django.contrib.auth import authenticate, login
		
class LoginForm(forms.Form):
	login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login', 'class': 'col-sm-6'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'col-sm-6'}))

	def auth_and_login(self, request):
		if (self.is_valid()):
			user = authenticate(username=self.cleaned_data['login'], password=self.cleaned_data['password'])
			if (user is not None):
				login(request, user)
				return True
		return False
				
#class LoginForm(forms.ModelForm):
#	class Meta:
#		model = User
#		fields = ('username', 'password')
#		labels = {'username': 'Login', 'password': 'Password'}
#		widgets = {	'username': forms.TextInput(attrs={'placeholder': 'Login', 'class': 'col-sm-6'}),
#					'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'col-sm-6'})
#				  }
		
class RegisterForm(forms.Form):
	login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login', 'class': 'col-sm-6'}))
	email = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'placeholder': 'E-mail', 'class': 'col-sm-6'}))	# EmailInput
	nickname = forms.CharField(label='Shown name', widget=forms.TextInput(attrs={'placeholder': 'Nickname', 'class': 'col-sm-6'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'col-sm-6'}))
	password_repeat = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password', 'class': 'col-sm-6'}))
	userpic = forms.FileField(label='Avatar', required=False, widget=forms.ClearableFileInput(attrs={'placeholder': 'C:\\Avatar.png', 'class': 'file-upload col-sm-6'}))
	
	def save(self, request):
		if (self.is_valid()):
			error_dict = self.checkDuplicates(username=self.cleaned_data['login'], nickname=self.cleaned_data['nickname'])
			if (error_dict):
				return False
			user = User.objects.create_user(username=self.cleaned_data['login'], email=self.cleaned_data['email'], password=self.cleaned_data['password'])
			#except IntegrityError:
			#	pass # User already exist!
			if (user is not None):
					extuser = ExtendedAskUser(
						user = user,
						nickname = self.cleaned_data['nickname'],
						userpic = self.cleaned_data['userpic']
					)
					#extuser.user = user
					#extuser.nickname = self.cleaned_data['nickname']
					#extuser.userpic = self.cleaned_data['userpic']
					extuser.save()
					return True
		return False
		
	def checkDuplicates(self, username, nickname):
		error_dict = {}
		try:
			user = User.objects.get(username=username) 
		except User.DoesNotExist:
			pass
		if (user):
			error_dict['login_exist'] = username
		try:
			extuser = ExtendedAskUser.objects.get(nickname=nickname)
		except ExtendedAskUser.DoesNotExist:
			pass
		if (extuser):
			error_dict['nickname_exist'] = nickname
		return error_dict
		
		
class QuestionForm(forms.Form):
	title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'col-sm-6'}))
	text = forms.CharField(label='Text', widget=forms.Textarea(attrs={'placeholder': 'Text of your question Google hasn\'t answered you', 'class': 'col-sm-6', 'rows':9}))
	tags = forms.CharField(label='Tags', widget=forms.TextInput(attrs={'placeholder': 'From 1 to 3', 'class': 'col-sm-6'}))
	
	def save(self, request):
		if (self.is_valid() and request.user.is_authenticated()):
			question = Question(
				author = request.user,
				title = self.cleaned_data['title'],
				text = self.cleaned_data['text']
			)
			question.save()
			question.tags.add(*self.checkTags(tags_string=self.cleaned_data['tags']))
			return True
		return False
		
	def checkTags(self, tags_string):
		tagName_list = [tag.strip() for tag in tags_string.split(',')]
		tag_list = []
		for tag in tagName_list:
			tag = "_".join(tag.split())
			tag_obj, created_bool = Tag.objects.get_or_create(tagName=tag)
			tag_list.append(tag_obj)
		return tag_list
		
class AnswerForm(forms.Form):
	text = forms.CharField(label='Text', widget=forms.Textarea(attrs={'placeholder': 'Text of your answer', 'class': 'col-sm-6', 'rows':4}))
	
	def save(self, request, question_id):
		if (self.is_valid()):
			try:
				question = Question.objects.get(id=question_id)
			except Question.DoesNotExist: # Honestly, should never be triggered
				raise Http404
			answer = Answer(
				author = request.user,
				text = self.cleaned_data['text'],
				question = question
			)
			answer.save()
			return True
		return False