from django.conf.urls import patterns, url

from imgup import views

urlpatterns = patterns('',
    url(r'^$', 'imgup.views.index', name='imgup.index'),
    url(r'^upload/$', 'imgup.views.upload_file', name='imgup.upload_file'),
    url(r'^login/$', 'imgup.views.user_login', name='imgup.login'),
    url(r'^logout/$', 'imgup.views.user_logout', name='imgup.logout'),
	url(r'^user/$', 'imgup.views.profile_view', name='imgup.profile_view'),
    url(r'^user/(?P<user_name>\w+)/$', 'imgup.views.profile_view', name='imgup.profile_view'),
    url(r'^delete/(?P<image_id>\d+)/$', 'imgup.views.delete_image', name='imgup.delete_image'),
)