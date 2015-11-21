from django.contrib import admin
from ask_app.models import ExtendedAskUser, Question, Answer, QuestionVote, AnswerVote, Tag
# Register your models here.

class AskAdmin(admin.ModelAdmin):
	list_display = ['ExtendedAskUser', 'Question', 'Answer', 'QuestionVote', 'AnswerVote', 'Tag']

admin.site.register(ExtendedAskUser)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionVote)
admin.site.register(AnswerVote)
admin.site.register(Tag)
