from django.conf.urls import patterns, url
from table.views import table_list

urlpatterns = patterns('',
	url(
		regex = r'^table/(\d+)$',
		view = table_list,
		name = "table_list"
	),
)