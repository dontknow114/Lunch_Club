from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import date, datetime
import calendar


class NutritionCategory(models.Model):
	"""
	Model representing a book genre (e.g. Science Fiction, Non Fiction).
	"""
	name = models.CharField(max_length=200, help_text="Enter the nutritional category for the Lunch.")    
	
	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Recipe(models.Model):

	recipe_name = models.CharField(max_length=200)
	chef = models.ForeignKey(User)
	description = models.TextField(max_length=1000, help_text="Enter a brief description of the lunch")
	nutritioncategory = models.ManyToManyField(NutritionCategory, help_text="Select a nutrition category for this book")
	recipe_image = models.ImageField(upload_to='', null=True, blank=True)

	def __str__(self):
		return self.recipe_name
	
	def get_absolute_url(self):
		return reverse('recipe-detail', args=[str(self.id)])
	def get_absolute_url_edit(self):
		return reverse('recipe-edit', args=[str(self.id)])
	def get_absolute_url_delete(self):
		return reverse('recipe-delete', args=[str(self.id)])

	def display_nutcat(self):
		"""
		Creates a string for the Genre. This is required to display genre in Admin.
		"""
		return ', '.join([ nutritioncategory.name for nutritioncategory in self.nutritioncategory.all()[:5]])

	display_nutcat.short_description = 'NutritionCategory'


import uuid # Required for unique book instances
class Lunch(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular lunch across all lunches served and planned")
	recipe = models.ForeignKey('Recipe', on_delete=models.SET_NULL, null=True) 
	information = models.TextField(max_length=1000)
	serve_date = models.DateField(null=True, blank=True)

	SERVE_STATUS = (
		('po', 'Planned Open'),
		('pc', 'Planned Closed'),
		('sd', 'Served'),
		('cd', 'Cancelled'),
	)

	status = models.CharField(max_length=2, choices=SERVE_STATUS, blank=True, default='po', help_text='Status of the Lunch Instance')

	class Meta:
		ordering = ["serve_date"]
		permissions = (("can_mark_served", "Set status as cd"),)  	

	def __str__(self):
		return '%s - %s - %s - %s' % (self.recipe.recipe_name, self.information, self.serve_date, self.status)
	def get_absolute_url(self):
		return reverse('lunch-detail', args=[str(self.id)])
	def get_absolute_url_edit(self):
		return reverse('lunch-edit', args=[str(self.id)])
	def get_absolute_url_delete(self):
		return reverse('lunch-delete', args=[str(self.id)])

	def lunch_weekday(self):
		lunch_weekday = calendar.day_name[date(self.serve_date.year, self.serve_date.month, self.serve_date.day).weekday()]
		return lunch_weekday
	def lunch_weekday_num(self):
		lunch_weekday_num = date(self.serve_date.year, self.serve_date.month, self.serve_date.day).weekday()
		return lunch_weekday_num

@property
def is_overdue(self):
	if self.serve_date > date.today():
		return True
	return False


class Arrangement(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular transaction for this lunch instance")
	gastronome = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	kudos_amount = models.IntegerField(help_text = "Amount for this transaction")

	SERVE_STATUS_CHEF = (
		('P', 'Planned'),
		('S', 'Served'),
		('C', 'Cancelled'),
		('D', 'Disputed'),
	)
	SERVE_STATUS_GASTRONOME = (
		('R', 'Reserved'),
		('V', 'Received'),
		('C', 'Cancelled'),
		('D', 'Disputed'),
	)

	serve_status_chef = models.CharField(max_length=1, choices=SERVE_STATUS_CHEF, blank=True, default='P', help_text='Status of the lunch provided')
	serve_status_gastronome = models.CharField(max_length=1, choices=SERVE_STATUS_GASTRONOME, blank=True, default='R', help_text='Status of the lunch reserved')
	lunch = models.ForeignKey('Lunch', on_delete=models.SET_NULL, null=True)

	def get_absolute_url(self):
		return reverse('arrangement-detail', args=[str(self.id)])

	def __str__(self):
		return '%s %s %s' % (self.lunch.recipe.chef.username, self.gastronome, self.lunch)


class Profile(models.Model):
	user = models.OneToOneField(User)
	bio = models.TextField(max_length=500, blank=True)

	def get_absolute_url(self):
		return reverse('user-profile', args=[str(self.id)])
