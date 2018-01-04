from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
# Create your models here.


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

class Lunch(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    lunchname = models.CharField(max_length=200)
    chef = models.ForeignKey('Chef', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the lunch")
    nutritioncategory = models.ManyToManyField(NutritionCategory, help_text="Select a nutrition category for this book")
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.    

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.lunchname
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('lunch-detail', args=[str(self.id)])

    def display_nutcat(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ nutritioncategory.name for nutritioncategory in self.nutritioncategory.all()[:5]])

    display_nutcat.short_description = 'NutritionCategory'


import uuid # Required for unique book instances
class LunchInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular lunch across all lunches served and planned")
    lunch = models.ForeignKey('Lunch', on_delete=models.SET_NULL, null=True) 
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
        """
        String for representing the Model object
        """
        return '%s - %s - %s - %s' % (self.lunch.lunchname, self.information, self.serve_date, self.status)


@property
def is_overdue(self):
	if self.serve_date > date.today():
		return True
	return False



class Chef(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('chef-detail', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Chef.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.chef.save()


class Arrangement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular transaction for this lunch instance")

    gastronome = models.ForeignKey('Chef', on_delete=models.SET_NULL, null=True, related_name='gastronome_arrangement')
    serve_date = models.DateField(null=True, blank=True)
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
    lunchinstance = models.ForeignKey('LunchInstance', on_delete=models.SET_NULL, null=True)


    def get_absolute_url(self):
        return reverse('arrangement-detail', args=[str(self.id)])

    def __str__(self):
        return '%s %s %s' % (self.lunchinstance.lunch.chef, self.gastronome, self.lunchinstance)



