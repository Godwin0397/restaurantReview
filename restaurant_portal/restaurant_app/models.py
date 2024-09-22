from django.db import models
from django.utils import timezone

# Create your models here.


class Chef(models.Model):
    
    """
    To store information about Chef
    """

    name = models.CharField(max_length=200, null=True)
    specialist = models.TextField(null=True)
    college = models.TextField(null=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):

    """
    To store information about Restaurant
    """

    restaurant = models.CharField(max_length=200)
    restaurantType = models.TextField()
    location = models.TextField()
    chefName = models.ForeignKey(Chef, related_name="restaurant_chef", on_delete=models.CASCADE)


class RestaurantReview(models.Model):

    """
    To store information about restaurants review
    """
    
    restaurantName = models.ForeignKey(Restaurant, related_name="restaurant_review", on_delete=models.CASCADE)
    review = models.TextField()
