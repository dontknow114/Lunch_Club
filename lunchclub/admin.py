from django.contrib import admin
from .models import NutritionCategory, Lunch, LunchInstance, Arrangement #,Chef

#admin.site.register(Lunch)
#admin.site.register(Chef)
admin.site.register(NutritionCategory)
#admin.site.register(LunchInstance)


class LunchInline(admin.TabularInline):
	model = Lunch
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

class LunchInstanceInline(admin.TabularInline):
	model = LunchInstance
	extra = 1

# Register the Admin classes for Book using the decorator
@admin.register(Lunch)
class LunchAdmin(admin.ModelAdmin):
	list_display = ('lunchname', 'chef', 'display_nutcat')
	inlines = [LunchInstanceInline]

	fieldsets = (
		('test', {
		    'fields': ('lunchname', 'chef', 'description', 'nutritioncategory')
		}),
	)

# Register the Admin classes for BookInstance using the decorator

@admin.register(LunchInstance) 
class LunchInstanceAdmin(admin.ModelAdmin):
	list_filter = ('status', 'serve_date')
	list_display = ('lunch', 'information','serve_date', 'status')
	
	fieldsets = (
		('Lunch Information', {
		    'fields': ('lunch', 'information')
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
	list_display = ('id','gastronome','lunchname','lunchinstanceinfo')

	def lunchname(self, obj):
		return obj.lunchinstance.lunch.lunchname
	def chef(self, obj):
		return obj.lunchinstance.lunch.chef
	def lunchinstanceinfo(self, obj):
		return obj.lunchinstance.information
	

