from django.conf.urls import url

from . import views


urlpatterns = [

	url(r'^$', views.index, name='index'),
	url(r'^lunchlist/$', views.LunchListView.as_view(), name = 'lunchlist'),
	url(r'^lunch/(?P<pk>\d+)$', views.LunchDetailView.as_view(), name='lunch-detail'),

	url(r'^cheflist/$', views.ChefListView.as_view(), name = 'cheflist'),
	url(r'^chef/(?P<pk>\d+)$', views.ChefDetailView.as_view(), name='chef-detail'),

	url(r'^arrangementlist/$', views.ArrangementListView.as_view(), name = 'arrangementlist'),
	url(r'^arrangement/(?P<pk>[^/]+)$', views.ArrangementDetailView.as_view(), name='arrangement-detail'),

]




urlpatterns += [   
    url(r'^mylunches/$', views.LunchesByUserListView.as_view(), name='my-lunches'),
]

urlpatterns += [   
    url(r'^grouplunches/$', views.LunchesByGroupListView.as_view(), name='group-lunches'),
]

urlpatterns += [   
    url(r'^lunch/(?P<pk>[-\w]+)/renew/$', views.renew_lunch_chef, name='lunch-renew-chef'),
]