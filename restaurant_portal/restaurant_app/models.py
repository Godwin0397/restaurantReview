from django.db import models
from django.utils import timezone

# Create your models here.


class CineProfessionls(models.Model):
    
    """
    To store information about Cine professionals
    """

    name = models.CharField(max_length=200, null=True)
    profile = models.TextField(null=True)
    date_of_birth = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def name_length(self):
        return len(self.name)


class Movie(models.Model):

    """
    To store information about movies
    """

    title = models.CharField(max_length=200)
    plot = models.TextField()
    cast = models.ManyToManyField(CineProfessionls, related_name="movie_cast")
    producer = models.ForeignKey(CineProfessionls, related_name="movie_producer", on_delete=models.CASCADE)
    director = models.ForeignKey(CineProfessionls, related_name="movie_director", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class MovieReview(models.Model):

    """
    To store information about movies review
    """
    
    movie = models.ForeignKey(Movie, related_name="movie_review", on_delete=models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return self.review











