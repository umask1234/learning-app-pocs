from django.db import models

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    liked_books = models.ManyToManyField(Book, blank=True)

