from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    source = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Note(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    selected_text = models.TextField(blank=True)
    note_text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.note_text
