from django.contrib import admin
from restaurant_app.models import Employees, Restaurant, RestaurantReview

# Register your models here.

admin.site.register(Employees)
admin.site.register(Restaurant)
admin.site.register(RestaurantReview)