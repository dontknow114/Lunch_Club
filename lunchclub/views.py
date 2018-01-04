from django.shortcuts import render
from datetime import date
import calendar

# Create your views here.

from .models import NutritionCategory, Lunch, LunchInstance, Chef, Arrangement

def index(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_lunches = Lunch.objects.all().count()
	num_instances = LunchInstance.objects.all().count()
	# Available books (status = 'a')
	num_instances_available = LunchInstance.objects.filter(status__exact = 'po').count()
	num_instances_planned_closed = LunchInstance.objects.filter(status__exact = 'pc').count()
	num_instances_served = LunchInstance.objects.filter(status__exact = 'sd').count()
	num_chefs = Chef.objects.all().count()  # The 'all()' is implied by default.



	var_username = None
	if request.user.is_authenticated():
		var_username = request.user.username

	cur_user_lunches = Lunch.objects.filter(chef__user__username__exact = var_username)

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
						'num_instances':num_instances,
						'num_instances_available':num_instances_available,
						'num_instances_served':num_instances_served,
						'num_chefs':num_chefs,
						'num_nutrition_category':num_nutrition_category,
						'num_visits':num_visits,
						'cur_user_lunches':cur_user_lunches,
						'var_username':var_username
					},
	)


from django.views import generic

class LunchListView(generic.ListView):
	model = Lunch
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super(LunchListView, self).get_context_data(**kwargs)
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

class LunchDetailView(generic.DetailView):
	model = Lunch

class ChefListView(generic.ListView):
	model = Chef
#    paginate_by = 5

class ChefDetailView(generic.DetailView):
	model = Chef

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
	model = LunchInstance
	template_name ='lunchclub/lunchinstance_list_applied_user.html'
	paginate_by = 2

	def get_queryset(self):
	#        return LunchInstance.objects.filter(gastronome=self.request.user).filter(status__exact='o').order_by('due_back')
		return LunchInstance.objects.filter(lunch__chef__user__username=self.request.user).order_by('serve_date')



from django.contrib.auth.mixins import PermissionRequiredMixin

class LunchesByGroupListView(PermissionRequiredMixin,generic.ListView):
	permission_required = 'lunchclub.can_mark_served'
	model = LunchInstance
	template_name ='lunchclub/lunchinstance_list_applied_group.html'
	def get_queryset(self):
	#        return LunchInstance.objects.filter(gastronome=self.request.user).filter(status__exact='o').order_by('due_back')
		return LunchInstance.objects.all().order_by('serve_date')
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
	lunch_inst=get_object_or_404(LunchInstance, pk = pk)

	# If this is a POST request then process the Form data
	if request.method == 'POST':

		# Create a form instance and populate it with data from the request (binding):
		form = ChangeLunchDate(request.POST)

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			lunch_inst.due_back = form.cleaned_data['lunch_date']
			lunch_inst.save()

			# redirect to a new URL:
			return HttpResponseRedirect(reverse('my-lunches') )

	# If this is a GET (or any other method) create the default form.
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = ChangeLunchDate(initial={'lunch_date': proposed_renewal_date,})

	return render(request, 'lunchclub/lunch_renew_chef.html', {'form': form, 'lunchinst':lunch_inst})