from django.conf.urls.defaults import *

from appman.models import *

urlpatterns = patterns('appman.views',
	(r'^app/list/$', 'application_list'),
	(r'^app/add/$', 'application_form'),
	(r'^app/(?P<object_id>\d+)/$', 'application_detail'), 
)