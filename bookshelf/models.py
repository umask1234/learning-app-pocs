from django.db import models
# from django.contrib.postgres.fields import ArrayField

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    # liked_books = ArrayField(
    #     models.IntegerField(),
    #     blank=True,             # Allows the field to be empty
    #     null=True,              # Allows the field to store NULL values in the database
    #     default=list
    # )

class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
