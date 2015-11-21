from django import forms

class UserForm(forms.Form)
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	email = forms.CharField()	#EmailIpnut
	password = forms.CharField() #PasswordIpnut
	
	def save()
		user_create(...)
		user.save()