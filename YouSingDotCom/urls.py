from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from YouSingDotCom.settings import DEBUG
from songthread.views import SongthreadListView, SongthreadDetailView, SongthreadCreateView, SongCreateView
from django.contrib.auth.decorators import login_required
import vote.views as vote_views

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', SongthreadListView.as_view(), name='songthread_list'),
    url(r'^thread/add/$', SongthreadCreateView.as_view(), name='songthread_create'),
    url(r'^thread/(?P<pk>\d+)/$', SongthreadDetailView.as_view(), name='songthread_detail'),
    url(r'^song/add/(?P<songthread_id>\d+)/$', SongCreateView.as_view(), name='song_create'),
    url(r'^vote/(?P<song_id>\d+)/(?P<like>\d+)/$', login_required(vote_views.vote), name='vote_create'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),

)

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

