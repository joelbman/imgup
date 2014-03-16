from django.conf.urls import patterns, url

from imgup import views

urlpatterns = patterns('',
    url(r'^$', 'imgup.views.index', name='imgup.index'),
    url(r'^upload/$', 'imgup.views.upload_file', name='imgup.upload_file'),
    url(r'^login/$', 'imgup.views.user_login', name='imgup.login'),
    url(r'^logout/$', 'imgup.views.user_logout', name='imgup.logout'),
    url(r'^user/(?P<user_id>\d+)/$', 'imgup.views.profile_view_index', name='imgup.profile_view_index'),
)