from django.db import models
from django.utils import timezone

# Create your models here.


class Employees(models.Model):
    
    """
    To store information about Employees
    """

    name = models.CharField(max_length=200, null=True)
    role = models.TextField(null=True)
    qualification = models.TextField(null=True)

    def __str__(self):
        return self.name

    @property
    def name_length(self):
        return len(self.name)

class Restaurant(models.Model):

    """
    To store information about Restaurant
    """

    restaurant = models.CharField(max_length=200)
    restaurantType = models.TextField()
    location = models.TextField()
    waiters = models.ManyToManyField(Employees, related_name="restaurant_waiters")
    manager = models.ForeignKey(Employees, related_name="restaurant_Manager", on_delete=models.CASCADE)
    chefName = models.ForeignKey(Employees, related_name="restaurant_chef", on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant


class RestaurantReview(models.Model):

    """
    To store information about restaurants review
    """
    
    restaurantName = models.ForeignKey(Restaurant, related_name="restaurant_review", on_delete=models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return self.review
    
    @property
    def review_length(self):
        return len(self.review)