from django.shortcuts import render
from datetime import date, datetime
import calendar


# Create your views here.

from .models import NutritionCategory, Recipe, Lunch, Arrangement #, Chef
from django.contrib.auth.models import User 
from django.views import generic

def index(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_recipes = Recipe.objects.all().count()
	num_lunches = Lunch.objects.all().count()
	num_lunches_all = Lunch.objects.all()
	# Available books (status = 'a')
	num_lunches_available = Lunch.objects.filter(status__exact = 'po').count()
	num_lunches_planned_closed = Lunch.objects.filter(status__exact = 'pc').count()
	num_lunches_served = Lunch.objects.filter(status__exact = 'sd').count()
	# num_chefs = Chef.objects.all().count()  # The 'all()' is implied by default.
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

def nextweek(request):
	datechoice = request.GET['datechoice']
	lastweek = date.today() - datetime.timedelta(days=int(datechoice))
	nextweek = date.today() + datetime.timedelta(days=int(datechoice))
	togglenextweek = int(datechoice) + 7
	togglelastweek = int(datechoice) - 7

	return render(
		request,
		'lunchclub/nextweek.html',
		context =	{
						'datechoice':datechoice,
						'prevweek':lastweek,
						'nextweek':nextweek,
						'togglenextweek':togglenextweek,
						'togglelastweek':togglelastweek,
					},
	)
	#Code to filter products whose price is less than price_lte i.e. 5000



class thisweekListView(generic.ListView):

	model = Lunch
	template_name ='lunchclub/thisweek.html'


	

	def get_queryset(self):
	#        return LunchInstance.objects.filter(gastronome=self.request.user).filter(status__exact='o').order_by('due_back')
		var1 = datetime.datetime.today().weekday()
		return Lunch.objects.filter(serve_date__range=(date.today(), date.today() + datetime.timedelta(days=60) - datetime.timedelta(days=var1) )).order_by('serve_date')

	def get_context_data(self, **kwargs):
		context = super(thisweekListView, self).get_context_data(**kwargs)
#		context['test'] = datetime.datetime.today().weekday()
#		context['week'] = (('Monday',1),'Tuesday','Wednesday','Thursday','Friday')

		var_monday = date.today() - datetime.timedelta(days=datetime.datetime.today().weekday())
		var_monday_str = var_monday.strftime("%b %d")
		var_tue = var_monday + datetime.timedelta(days=1)
		var_wed = var_monday + datetime.timedelta(days=2)
		var_thu = var_monday + datetime.timedelta(days=3)
		var_fri = var_monday + datetime.timedelta(days=4)

		context['thisweek'] =	{
									'Mon - ' + var_monday_str:Lunch.objects.filter(serve_date = var_monday),
									'Tue - ' + var_tue.strftime("%b %d"):Lunch.objects.filter(serve_date = var_monday + datetime.timedelta(days=1)),
									'Wed - ' + var_wed.strftime("%b %d"):Lunch.objects.filter(serve_date = var_monday + datetime.timedelta(days=2)),
									'Thu - ' + var_thu.strftime("%b %d"):Lunch.objects.filter(serve_date = var_monday + datetime.timedelta(days=3)),
									'Fri - ' + var_thu.strftime("%b %d"):Lunch.objects.filter(serve_date = var_monday + datetime.timedelta(days=4))
								}
		return context



		context['test'] =		{
									'Key1' : { 'SubKey1' : 'SubVal1' },
									'Key2' : { 'SubKey2' : 'SubVal2' }
								}
		return context




class RecipeListView(generic.ListView):
	model = Recipe
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super(RecipeListView, self).get_context_data(**kwargs)
		context['weekday'] = calendar.day_name[date.today().weekday()]
		return context

#	context_object_name = "unch"
#	queryset = Lunch.objects.prefetch_related('nutritioncategory')


	#context_object_name = 'my_book_list'   # your own name for the list as a template variable
	#queryset = Lunch.objects.filter(name__icontains='k')[:5] # Get 5 books containing the title war
	#template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
	
	#def get_queryset(self):
	#	return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war

#	def get_context_data(self, **kwargs):
#		# Call the base implementation first to get a context
#		context = super(BookListView, self).get_context_data(**kwargs)
#		# Get the blog from id and add it to the context
#		context['some_data'] = 'This is just some data'
#		return context

class RecipeDetailView(generic.DetailView):
	model = Recipe

class ChefListView(generic.ListView):
	model = User

class ChefDetailView(generic.DetailView):
	model = User

class LunchListView(generic.ListView):
	model = Lunch
	paginate_by = 10

	def get_context_data(self, **kwargs):		

		context = super(LunchListView, self).get_context_data(**kwargs)

		return context

class LunchDetailView(generic.DetailView):
	model = Lunch

class ArrangementListView(generic.ListView):
	model = Arrangement
	paginate_by = 10

class ArrangementDetailView(generic.DetailView):
	model = Arrangement

from django.contrib.auth.mixins import LoginRequiredMixin

class LunchesByUserListView(LoginRequiredMixin,generic.ListView):
	"""
	Generic class-based view listing books on loan to current user. 
	"""
	model = Lunch
	template_name ='lunchclub/lunch_list_applied_user.html'
	paginate_by = 2

	def get_queryset(self):
	#        return LunchInstance.objects.filter(gastronome=self.request.user).filter(status__exact='o').order_by('due_back')
		return Lunch.objects.filter(recipe__chef=self.request.user).order_by('serve_date')



from django.contrib.auth.mixins import PermissionRequiredMixin

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





from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import datetime


from .forms import ChangeLunchDate

#@permission_required('catalog.can_mark_returned')
def renew_lunch_chef(request, pk):
	"""
	View function for renewing a specific BookInstance by librarian
	"""
	lunch = get_object_or_404(Lunch, pk = pk)

	# If this is a POST request then process the Form data
	if request.method == 'POST':

		# Create a form instance and populate it with data from the request (binding):
		form = ChangeLunchDate(request.POST)

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			lunch.serve_date = form.cleaned_data['serve_date']
			lunch.save()

			# redirect to a new URL:
			return HttpResponseRedirect(reverse('my-lunches') )

	# If this is a GET (or any other method) create the default form.
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = ChangeLunchDate(initial={'serve_date': proposed_renewal_date,})

	return render(request, 'lunchclub/lunch_renew_chef.html', {'form': form, 'lunch':lunch})



