from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(date.today().year)]
    )
    director = models.ForeignKey('Person', related_name='directed_movies')
    writer = models.ForeignKey('Person', blank=True, null=True, related_name='wrote_movies')
    actors = models.ManyToManyField('Person', blank=True, null=True, related_name='acted_movies')
    fun_fact = models.CharField(max_length=500, blank=True, null=True)

    distributor = models.ForeignKey('Distributor', blank=True, null=True)
    production_company = models.ForeignKey('ProductionCompany', blank=True, null=True)


    class Meta:
        unique_together = ('title', 'year', 'director')


class Location(models.Model):
    movie = models.ForeignKey(Movie, related_name='locations')
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(validators=[MinValueValidator(-0.0), MaxValueValidator(90.0)], decimal_places=2, max_digits=4)
    longitude = models.DecimalField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)], decimal_places=2, max_digits=5)
    class Meta:
        unique_together = ('movie', 'name')
        select_on_save = True

class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)

class ProductionCompany(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Distributor(models.Model):
    name = models.CharField(max_length=255, unique=True)