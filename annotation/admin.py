from django.contrib import admin

# Register your models here.

from .models import Article, Note

admin.site.register(Article)
admin.site.register(Note)
