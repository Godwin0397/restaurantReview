from django.contrib import admin
from restaurant_app.models import Chef, Restaurant, RestaurantReview

# Register your models here.

admin.site.register(Chef)
admin.site.register(Restaurant)
admin.site.register(RestaurantReview)