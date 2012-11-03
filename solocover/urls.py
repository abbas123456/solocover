from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from solocover.settings import DEBUG
from songthread.views import SongthreadListView, SongthreadDetailView, \
    SongthreadCreateView, SongCreateView, CommentCreateView
from django.contrib.auth.decorators import login_required
from vote.views import VoteCreateView
from solocover.views import LandingPageView, AboutPageView
from account.views import UserCreateView, UserUpdateView, UserDetailView
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from songthread.models import Songthread
from account.models import UserProfile
from solocover.sitemap import StaticSitemap

songthread_info_dict = {
    'queryset': Songthread.objects.all(),
    'date_field': 'created_date',
}
userprofile_info_dict = {
    'queryset': UserProfile.objects.all(),
}

sitemaps = {
    'threads': GenericSitemap(songthread_info_dict, changefreq='Daily'),
    'users': GenericSitemap(userprofile_info_dict, changefreq='Daily'),
    'main': StaticSitemap,
}

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', LandingPageView.as_view(), name='landing_page'),
    url(r'^about/$', AboutPageView.as_view(), name='about_page'),
    url(r'^threads/$', SongthreadListView.as_view(), name='songthread_list'),
    url(r'^thread/add/$', SongthreadCreateView.as_view(),
        name='songthread_create'),
    url(r'^thread/(?P<slug>[-\w\d]+)/(?P<pk>\d+)/$',
        SongthreadDetailView.as_view(), name='songthread_detail'),
    url(r'^song/add/(?P<songthread_id>\d+)/$',
        login_required(SongCreateView.as_view()), name='song_create'),
    url(r'^vote/(?P<song_id>\d+)/(?P<like>\d+)/$',
        login_required(VoteCreateView.as_view()), name='vote_create'),
    url(r'^comment/(?P<songthread_id>\d+)/$', CommentCreateView.as_view(),
        name='comment_create'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        name='logout'),
    url(r'^accounts/register/$', UserCreateView.as_view(), name='register'),
    url(r'^accounts/profile/$', UserUpdateView.as_view(),
        name='edit_profile'),
    url(r'^view-profile/(?P<slug>[-\w\d]+)/(?P<pk>\d+)/$',
        UserDetailView.as_view(), name='view_profile'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps})

)

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.
                          MEDIA_ROOT)
