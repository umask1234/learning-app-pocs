from django.contrib import admin

# Register your models here.

from .models import Book, User

admin.site.register(Book)
admin.site.register(User)