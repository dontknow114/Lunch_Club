from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from datetime import date, datetime
import calendar
import datetime

from .models import NutritionCategory, Recipe, Lunch, Arrangement, Profile


def index(request):
	num_recipes = Recipe.objects.all().count()
	num_lunches = Lunch.objects.all().count()
	num_lunches_all = Lunch.objects.all()
	num_lunches_available = Lunch.objects.filter(status__exact = 'po').count()
	num_lunches_planned_closed = Lunch.objects.filter(status__exact = 'pc').count()
	num_lunches_served = Lunch.objects.filter(status__exact = 'sd').count()
	num_users = User.objects.all().count()

	var_username = None
	if request.user.is_authenticated():
		var_username = request.user.username

	cur_user_recipes = Recipe.objects.filter(chef__username__exact = var_username).count()

	# Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	num_nutrition_category = NutritionCategory.objects.all().count()
	
	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'index.html',
		context =	{
						'num_lunches':num_lunches,
						'num_recipes':num_recipes,
						'num_lunches_available':num_lunches_available,
						'num_lunches_served':num_lunches_served,
						# 'num_chefs':num_chefs,
						'num_nutrition_category':num_nutrition_category,
						'num_visits':num_visits,
						'cur_user_recipes':cur_user_recipes,
						'var_username':var_username,
						'num_users':num_users,
						'num_lunches_all':num_lunches_all,
					},
	)


#################### Special Non-Generic Views ####################
def weekview(request):

	datechoice = request.GET['datechoice']
	var_mon = date.today() - datetime.timedelta(days=datetime.datetime.today().weekday()) + datetime.timedelta(days=7)
	next_week = var_mon + datetime.timedelta(days=int(datechoice))
	prev_week = next_week - datetime.timedelta(days=7)
	toggle_next_week = int(datechoice) + 7
	toggle_prev_week = int(datechoice) - 7

	all_lunch_objects = Lunch.objects.filter(serve_date__range=(prev_week, next_week)).order_by('serve_date')
	var_tue = prev_week + datetime.timedelta(days=1)
	var_wed = prev_week + datetime.timedelta(days=2)
	var_thu = prev_week + datetime.timedelta(days=3)
	var_fri = prev_week + datetime.timedelta(days=4)

	return render(
		request,
		'lunchclub/weekview.html',
		context =	{
						'datechoice':datechoice,
						'prev_week':prev_week,
						'next_week':next_week,
						'toggle_next_week':toggle_next_week,
						'toggle_prev_week':toggle_prev_week,
						'weekdays':
							{
								'Monday':Lunch.objects.filter(serve_date__range=(prev_week, prev_week)).order_by('serve_date'),
								'Tuesday':Lunch.objects.filter(serve_date__range=(var_tue,var_tue)).order_by('serve_date'),
								'Wednesday':Lunch.objects.filter(serve_date__range=(var_wed,var_wed)).order_by('serve_date'),
								'Thursday':Lunch.objects.filter(serve_date__range=(var_thu,var_thu)).order_by('serve_date'),
								'Friday':Lunch.objects.filter(serve_date__range=(var_fri,var_fri)).order_by('serve_date'),
							},
					},
		)



############################## RECIPE GENERIC VIEWS ##############################
class RecipeListView(generic.ListView):
	model = Recipe

	def get_context_data(self, **kwargs):
		context = super(RecipeListView, self).get_context_data(**kwargs)
		context['weekday'] = calendar.day_name[date.today().weekday()]
		return context


class RecipeDetailView(generic.DetailView):
	model = Recipe



############################## USER GENERIC VIEWS ##############################
class ChefListView(generic.ListView):
	model = User

class ChefDetailView(generic.DetailView):
	model = User

class UserDetailView(generic.DetailView):
	model = Profile



############################## LUNCH GENERIC VIEWS ##############################
class LunchListView(generic.ListView):
	model = Lunch
	paginate_by = 10

	def get_context_data(self, **kwargs):		
		context = super(LunchListView, self).get_context_data(**kwargs)
		return context


class LunchDetailView(generic.DetailView):
	model = Lunch



############################## ARRANGEMENT GENERIC VIEWS ##############################
class ArrangementListView(generic.ListView):
	model = Arrangement
	paginate_by = 10
class ArrangementDetailView(generic.DetailView):
	model = Arrangement



############################## DYNAMIC USER FILTERED VIEWS ##############################
class RecipesByUserListView(LoginRequiredMixin,generic.ListView):
	model = Recipe
	#template_name ='lunchclub/recipes_by_user.html'

	def get_queryset(self):
		return Recipe.objects.filter(chef = self.request.user)#.order_by('serve_date')


class LunchesByUserListView(LoginRequiredMixin,generic.ListView):
	model = Lunch
	#template_name ='lunchclub/lunches_by_user.html'

	def get_queryset(self):
		return Lunch.objects.filter(recipe__chef = self.request.user).order_by('serve_date')


class LunchesByGroupListView(PermissionRequiredMixin,generic.ListView):
	permission_required = 'lunchclub.can_mark_served'
	model = Lunch
	template_name ='lunchclub/lunchinstance_list_applied_group.html'
	def get_queryset(self):
	#        return LunchInstance.objects.filter(gastronome=self.request.user).filter(status__exact='o').order_by('due_back')
		return Lunch.objects.all().order_by('serve_date')
	# Or multiple permissions
	#permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
	# Note that 'catalog.can_edit' is just an example
	# the catalog application doesn't have such permission!




def testview(request):

	return render(
		request,
		'lunchclub/test.html',
		context =	{
						'data':'data',
					},
		)



############################ FORM SECTION #####################################################################
from django.shortcuts import redirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy



############################## RECIPE FORMS ##############################
from .forms import FormRecipeCreate
def recipe_create(request):
	if request.method == "POST":
		form = FormRecipeCreate(request.user, request.POST)
		if form.is_valid():
			recipe = form.save(commit=False)
			recipe.chef = request.user
			#post.published_date = timezone.now()
			recipe.save()
			form.save_m2m()
			return redirect('recipe-detail', pk=recipe.pk)
	else:
		form = FormRecipeCreate(request.user)
	return render(request, 'lunchclub/recipe_create.html', {'form': form})


from .forms import FormRecipeEdit
def recipe_edit(request, pk):
	recipe = get_object_or_404(Recipe, pk=pk)
	if request.method == "POST":
		form = FormRecipeEdit(request.POST, instance=recipe)
		if form.is_valid():
			recipe.save()
			return redirect('recipe-detail', pk=recipe.pk)
	else:
		form = FormRecipeEdit(instance=recipe)
	return render(request, 'lunchclub/recipe_edit.html', {'form': form})



class recipe_delete(DeleteView):
	model = Recipe
	success_url = reverse_lazy('my-recipes')



############################## LUNCH FORMS ##############################
from .forms import FormLunchCreate
def lunch_create(request):
	if request.method == "POST":
		form = FormLunchCreate(request.user, request.POST)
		if form.is_valid():
			lunch = form.save(commit=False)
			lunch.save()
			form.save_m2m()
			return redirect('lunch-detail', pk=lunch.pk)
	else:
		form = FormLunchCreate(request.user)
	return render(request, 'lunchclub/lunch_create.html', {'form': form})


from .forms import FormLunchEdit
def lunch_edit(request, pk):
	lunch = get_object_or_404(Lunch, pk=pk)
	recipe = lunch.recipe.recipe_name
	chef = lunch.recipe.chef.username
	weekday = lunch.lunch_weekday

	if request.method == "POST":
		form = FormLunchEdit(request.POST, instance=lunch)
		if form.is_valid():
			lunch.save()
			return redirect('lunch-detail', pk=lunch.pk)
	else:
		form = FormLunchEdit(instance=lunch)
	return render(request, 'lunchclub/lunch_edit.html', {
															'form': form,
															'recipe':recipe,
															'chef':chef,
															'weekday':weekday,
														}
		)


class lunch_delete(DeleteView):
	model = Lunch
	success_url = reverse_lazy('my-lunches')



############################## ARRANGEMENT FORMS ##############################