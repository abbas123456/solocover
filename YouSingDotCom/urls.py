from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import ListView

from YouSingDotCom.settings import DEBUG
from competition.models import Competition, Song
from competition.views import CompetitionDetailView, SongCreateView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^competitions/$', ListView.as_view(model=Competition), name='competition_list'),
    url(r'^competition/(?P<pk>\d+)/$', CompetitionDetailView.as_view(model=Competition), name='competition_detail'),
    url(r'^song/add/(?P<competition_id>\d+)/$', SongCreateView.as_view(), name='song_create'),
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
    
