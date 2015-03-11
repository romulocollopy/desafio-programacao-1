from django.conf.urls import patterns, url


urlpatterns = patterns('core.views',
    url(r'^$', 'home', name='home'),
    url(r'^upload-detail/(?P<id>[0-9]+)/$', 'upload_detail',
        name='upload_detail'),
)
