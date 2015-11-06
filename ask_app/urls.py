from django.conf.urls import url

urlpatterns = [
	url(r'^$', 'ask_app.views.main_page', name='main_page'),
	url(r'^hot/$', 'ask_app.views.hot_questions', name='hot_questions'),
	url(r'^tag/(?P<tag_name>\d\.+)/$', 'ask_app.views.tag', name='tag'),
	url(r'^questions/(?P<page_num>\d+)/$', 'ask_app.views.questions', name='questions'),
	url(r'^questions/$', 'ask_app.views.questions', name='questions'),
	url(r'^question/(?P<question_num>\d+)/$', 'ask_app.views.question', name='question'),
	url(r'^login/$', 'ask_app.views.login', name='login'),
	url(r'^register/$', 'ask_app.views.register', name='register'),
	url(r'^ask/$', 'ask_app.views.ask', name='ask'),
	url(r'^settings/$', 'ask_app.views.settings', name='settings'),
	url(r'^search/$', 'ask_app.views.search', name='search'),
	url(r'^logout/$', 'ask_app.views.logout', name='logout'),
	
]