
from django import forms


############### RECIPE FORMS SECTION ###############
from .models import Recipe, User
class FormRecipeCreate(forms.ModelForm):

	class Meta:
		model = Recipe
		fields = ('recipe_name', 'chef', 'description', 'nutritioncategory',)

#https://simpleisbetterthancomplex.com/questions/2017/03/22/
#how-to-dynamically-filter-modelchoices-queryset-in-a-modelform.html
	def __init__(self, user, *args, **kwargs):
		super(FormRecipeCreate, self).__init__(*args, **kwargs)
		self.fields['chef'].queryset = User.objects.filter(username=user)


class FormRecipeEdit(forms.ModelForm):

	class Meta:
		model = Recipe
		fields = ('recipe_name', 'chef', 'description', 'nutritioncategory',)


############### LUNCH FORMS SECTION ###############
from .models import Lunch
class FormLunchCreate(forms.ModelForm):

	class Meta:
		model = Lunch
		fields = ('recipe', 'information', 'serve_date', 'status',)

	#https://simpleisbetterthancomplex.com/questions/2017/03/22/
	#how-to-dynamically-filter-modelchoices-queryset-in-a-modelform.html
	def __init__(self, user, *args, **kwargs):
		super(FormLunchCreate, self).__init__(*args, **kwargs)
		self.fields['recipe'].queryset = Recipe.objects.filter(chef=user)


class FormLunchEdit(forms.ModelForm):

	class Meta:
		model = Lunch
		fields = ('serve_date','information',)



