from django.conf.urls import url

from desiquotes.quotes import views

app_name = 'quotes'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^user/$', views.user_quotes, name='user_quotes'),
    url(r'^user/name(?P<name>[-\w]+)$', views.user_quotes, name='user_name_quotes'),
    url(r'^author/name(?P<name>[-\w]+)$', views.user_quotes, name='user_quotes'),
    url(r'^user/write/$', views.CreateUserQuote.as_view(), name='add_user_quote'),
    url(r'^author/write/$', views.CreateAuthorQuote.as_view(), name='add_author_quote'),
    url(r'^user/edit/(?P<pk>\d+)/$', views.EditUserQuote.as_view(), name='edit_user_quote'),
    url(r'^author/edit/(?P<pk>\d+)/$', views.EditAuthorQuote.as_view(), name='edit_author_quote'),
    url(r'^home/$', views.home, name='home'),
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^remove/$', views.remove, name='remove'),
    url(r'^like/$', views.like, name='like'),
    url(r'^drafts/$', views.drafts, name='drafts'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    url(r'^(?P<slug>[-\w]+)/$', views.quote, name='quote'),
]
