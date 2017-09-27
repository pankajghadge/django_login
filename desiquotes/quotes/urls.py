from django.conf.urls import url

from desiquotes.quotes import views

urlpatterns = [
    url(r'^$', views.quotes, name='quotes'),
    url(r'^write/$', views.CreateQuote.as_view(), name='write'),
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^drafts/$', views.drafts, name='drafts'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    url(r'^edit/(?P<pk>\d+)/$',
        views.EditQuote.as_view(), name='edit_quote'),
    url(r'^(?P<slug>[-\w]+)/$', views.quote, name='quote'),
]
