from django.conf.urls import patterns, include, url
from django.contrib import admin
from YouSingDotCom.settings import DEBUG
from django.conf import settings
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^competitions/$', 'competition.views.list'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATICFILES_DIRS}
    ))
    
