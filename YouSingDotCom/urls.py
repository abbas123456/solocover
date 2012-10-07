from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from YouSingDotCom.settings import DEBUG
from songthread.views import SongthreadListView, SongthreadDetailView, SongthreadCreateView, SongCreateView, CommentCreateView
from django.contrib.auth.decorators import login_required
from vote.views import VoteCreateView
from YouSingDotCom.views import LandingPageView
from account.views import UserCreateView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', LandingPageView.as_view(), name='landing_page'),
    url(r'^threads/$', SongthreadListView.as_view(), name='songthread_list'),
    url(r'^thread/add/$', SongthreadCreateView.as_view(), name='songthread_create'),
    url(r'^thread/(?P<pk>\d+)/$', SongthreadDetailView.as_view(), name='songthread_detail'),
    url(r'^song/add/(?P<songthread_id>\d+)/$', SongCreateView.as_view(), name='song_create'),
    url(r'^vote/(?P<song_id>\d+)/$', login_required(VoteCreateView.as_view()), name='vote_create'),
    url(r'^comment/(?P<songthread_id>\d+)/$', CommentCreateView.as_view(), name='comment_create'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^accounts/register/$', UserCreateView.as_view(), name='register'),

)

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

