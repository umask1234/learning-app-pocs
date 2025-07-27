from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Article, Note
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note

# Create your views here.

def index(request):
    latest_article_list = Article.objects.order_by("-id")[:5]
    template = loader.get_template("annotation/index.html")
    context = {"latest_article_list": latest_article_list}
    return HttpResponse(template.render(context, request))

def articles(request, article_id=None):
    article = None if article_id is None else get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        title = request.POST.get("title")
        subtitle = request.POST.get("subtitle")
        author = request.POST.get("author")
        body = request.POST.get("body")
        source = request.POST.get("source")
        if not title.strip():
            return render(request, "annotation/articles.html", {
                "article": article,
                "error_message": "You didn't enter a title.",
            })
        if not author.strip():
            return render(request, "annotation/articles.html", {
                "article": article,
                "error_message": "You didn't enter an author.",
            })
        if not body.strip():
            return render(request, "annotation/articles.html", {
                "article": article,
                "error_message": "You didn't enter an article body.",
            })
        if not source.strip():
            return render(request, "annotation/articles.html", {
                "article": article,
                "error_message": "You didn't enter an article source.",
            })
        if article is None: # if user is creating a new note
            Article.objects.create(
                title = title,
                subtitle = subtitle, 
                author = author,
                body = body, 
                source = source
            )
        else: 
            article.title = title,
            article.subtitle = subtitle, 
            article.author = author,
            article.body = body, 
            article.source = source
            article.save()

        return redirect('article-index')
    return render(request, "annotation/articles.html", {
        "article": article if article else None,
    })

def detail(request, article_id):
    current_article = Article.objects.get(pk=article_id)
    template = loader.get_template("annotation/detail.html")
    context = {
        "article": current_article,
        "notes": current_article.note_set.all()
    }
    return HttpResponse(template.render(context, request))

def notes(request, article_id, note_id=None): # add and edit view (very similar!)
    article = get_object_or_404(Article, pk=article_id)
    note = None if note_id is None else get_object_or_404(Note, pk=note_id, article=article)
    
    if request.method == "POST":
        selected_text = request.POST.get("selected_text")
        note_text = request.POST.get("note_text")


        if not note_text.strip():
            return render(request, "annotation/notes.html", {
                "article": article,
                "error_message": "You didn't enter any note text.",
            })

        if note is None: # if user is creating a new note
            Note.objects.create(
                article=article,
                selected_text=selected_text or "",
                note_text=note_text
            )
        else: 
            note.selected_text = selected_text
            note.note_text = note_text
            note.save()

        return redirect("detail", article_id=article.id)

    if request.method == "GET":
        selected_text = note.selected_text if note else request.GET.get("selected_text", "")
        note_text = note.note_text if note else ""


    return render(request, "annotation/notes.html", {
        "article": article,
        "note": note, 
        "selected_text": note.selected_text if note else "", 
        "note_text": note.note_text if note else ""
    })
    
def delete_note(request, article_id, note_id):
    article = get_object_or_404(Article, pk=article_id)
    note = get_object_or_404(Note, pk=note_id, article=article)

    if request.method == "POST":
        note.delete()
        return redirect('detail', article_id=article_id)

    return render(request, "annotation/delete_confirm.html", {
        "note": note,
        "article": article
    })
