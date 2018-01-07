from django.contrib import admin
from .models import NutritionCategory, Lunch, Recipe, Arrangement #,Chef

#admin.site.register(Lunch)
#admin.site.register(Chef)
admin.site.register(NutritionCategory)
#admin.site.register(LunchInstance)


class RecipeInline(admin.TabularInline):
	model = Recipe
	extra = 0

# @admin.register(Chef)
# Define the admin class
# class ChefAdmin(admin.ModelAdmin):
	#this will add additional fields the list view of the chefs link
	# list_display = ('user',)
	# inlines = [LunchInline]
	# fields = ('user',)
	#fields = [('last_name', 'first_name')]
	#fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

class LunchInline(admin.TabularInline):
	model = Lunch
	extra = 1

# Register the Admin classes for Book using the decorator
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
	list_display = ('recipe_name', 'chef', 'display_nutcat', 'recipe_image')
	inlines = [LunchInline]

	fieldsets = (
		('Recipe', {
		    'fields': ('recipe_name', 'chef', 'description', 'nutritioncategory', 'recipe_image')
		}),
	)

# Register the Admin classes for BookInstance using the decorator

@admin.register(Lunch) 
class LunchAdmin(admin.ModelAdmin):
	list_filter = ('status', 'serve_date')
	list_display = ('recipe', 'information','serve_date', 'status')
	
	fieldsets = (
		('Recipe Information', {
		    'fields': ('recipe', 'information')
		}),
		('Lunch Status', {
		    'fields': ('status', 'serve_date')
		}),
		('Lunch ID', {
		    'fields': ('id', )
		}),
	)

@admin.register(Arrangement)
class ArrangementAdmin(admin.ModelAdmin):
	list_display = ('id','gastronome','lunchinfo')

	def recipe_name(self, obj):
		return obj.lunch.recipe
	def chef(self, obj):
		return obj.lunch.recipe.chef
	def lunchinfo(self, obj):
		return obj.lunch.information
	

