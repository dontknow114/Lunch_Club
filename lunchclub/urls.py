from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
]

########## Recipe URL Patterns ##########
urlpatterns += [
	url(r'^recipelist/$', views.RecipeListView.as_view(), name = 'recipelist'),
	url(r'^recipe/(?P<pk>\d+)$', views.RecipeDetailView.as_view(), name='recipe-detail'),
	url(r'^recipe/create/$', views.recipe_create, name='recipe-create'),
	url(r'^recipe/(?P<pk>[^/]+)/edit/$', views.recipe_edit, name='recipe-edit'),
	url(r'^recipe/(?P<pk>[^/]+)/delete/$', views.recipe_delete.as_view(), name='recipe-delete'),
]

########## Lunch URL Patterns ##########
urlpatterns += [
	url(r'^lunchlist/$', views.LunchListView.as_view(), name = 'lunchlist'),
	url(r'^lunch/(?P<pk>[0-9A-Fa-f-]+)$', views.LunchDetailView.as_view(), name='lunch-detail'),
	url(r'^lunch/create/$', views.lunch_create, name='lunch-create'),
	url(r'^lunch/(?P<pk>[^/]+)/edit/$', views.lunch_edit, name='lunch-edit'),
	url(r'^lunch/(?P<pk>[^/]+)/delete/$', views.lunch_delete.as_view(), name='lunch-delete'),
]

########## Arrangement URL Patterns ##########
urlpatterns += [
	url(r'^arrangementlist/$', views.ArrangementListView.as_view(), name = 'arrangementlist'),
	url(r'^arrangement/(?P<pk>[^/]+)$', views.ArrangementDetailView.as_view(), name='arrangement-detail'),
]
########## Dynamic User Filtered URL Patterns ##########
urlpatterns += [
	url(r'^mylunches/$', views.LunchesByUserListView.as_view(), name='my-lunches'),
	url(r'^myrecipes/$', views.RecipesByUserListView.as_view(), name='my-recipes'),
	url(r'^grouplunches/$', views.LunchesByGroupListView.as_view(), name='group-lunches'),
	url(r'^profile/(?P<pk>[^/]+)$', views.UserDetailView.as_view(), name='user-profile'),
]
########## Standard View URL Patterns ##########
urlpatterns += [
	url(r'^weekview/$', views.weekview, name='week-view'),
	url(r'^test/$', views.testview, name='test-view'),
]
