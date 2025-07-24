from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Article, Note

# Create your views here.

def index(request):
    latest_article_list = Article.objects.order_by("-id")[:5]
    template = loader.get_template("annotation/index.html")
    context = {"latest_article_list": latest_article_list}
    return HttpResponse(template.render(context, request))

def detail(request, article_id):
    current_article = Article.objects.get(pk=article_id)
    template = loader.get_template("annotation/detail.html")
    context = {
        "article": current_article,
        "notes": current_article.note_set.all()
    }
    return HttpResponse(template.render(context, request))
    return HttpResponse("You're looking at article %s." % article_id)
