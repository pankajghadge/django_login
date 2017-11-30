"""desiquotes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from desiquotes.core import views as core_views
from desiquotes.quotes import views as quotes_views
from desiquotes.authentication import views as quotes_auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     #url(r'^$', core_views.home, name='home'),
     url(r'^$', quotes_views.home, name='home'),
     url(r'^account/login', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
     url(r'^account/logout', auth_views.logout, {'template_name': 'core/logged_out.html'}, name='logout'),
     url(r'^account/password_reset/$', auth_views.password_reset, {'template_name': 'core/password_reset.html'}, name="password_reset"),
     url(r'^account/password_reset/done/$', auth_views.password_reset_done, {'template_name': 'core/password_reset_done.html'}, name='password_reset_done'),
     url(r'^account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
             auth_views.password_reset_confirm, {'template_name': 'core/password_reset_confirm.html'}, name='password_reset_confirm'),
     url(r'^account/password_reset/complete/$', auth_views.password_reset_complete, {'template_name': 'core/password_reset_complete.html'}, name='password_reset_complete'),
     url(r'^signup/$', quotes_auth_views.signup, name='signup'),

     url(r'^settings/$', core_views.settings, name='settings'),
     url(r'^settings/picture/$', core_views.picture, name='picture'),
     url(r'^settings/upload_picture/$', core_views.upload_picture, name='upload_picture'),
     url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture, name='save_uploaded_picture'),
     url(r'^settings/password/$', core_views.password, name='password'),

     url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),

     url(r'^quotes/', include('desiquotes.quotes.urls')),
     url(r'^admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
