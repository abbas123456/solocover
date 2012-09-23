from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import ListView

from YouSingDotCom.settings import DEBUG
from songthread.models import Songthread
from songthread.views import SongthreadDetailView, SongthreadCreateView, SongCreateView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^threads/$', ListView.as_view(model=Songthread), name='songthread_list'),
    url(r'^thread/add/$', SongthreadCreateView.as_view(), name='songthread_create'),
    url(r'^thread/(?P<pk>\d+)/$', SongthreadDetailView.as_view(), name='songthread_detail'),
    url(r'^song/add/(?P<songthread_id>\d+)/$', SongCreateView.as_view(), name='song_create'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),

)

if DEBUG:
    urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATICFILES_DIRS}
    ))
    
