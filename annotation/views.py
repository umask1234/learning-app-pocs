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

def detail(request, article_id):
    current_article = Article.objects.get(pk=article_id)
    template = loader.get_template("annotation/detail.html")
    context = {
        "article": current_article,
        "notes": current_article.note_set.all()
    }
    return HttpResponse(template.render(context, request))
    return HttpResponse("You're looking at article %s." % article_id)

# class NoteViewSet(viewsets.ModelViewSet):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

# class NotesView(APIView):
#     def get(self, request, article_id):
#         # notes = Note.objects.all()
#         notes = Note.objects.filter(article__id=article_id)
#         serializer = NoteSerializer(notes, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

def notes(request, article_id):
    # article = get_object_or_404(Article, pk=article_id)
    # try:
    #     selected_note = article.note_set.get(pk=request.POST["notes"])
    #     # selected_note = question.choice_set.get(pk=request.POST["notes"])
    # except (KeyError, Note.DoesNotExist):
    #     return render(
    #         request,
    #         "annotation/notes.html",
    #         {
    #             "article": article,
    #             "error_message": "Error! No note selected!",
    #         },
    #     )
    # else:
    #     # selected_note.votes = F("votes") + 1
    #     selected_note.note_text = request.note_text
    #     selected_note.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse("annotation:detail", args=(article.id,)))

    article = get_object_or_404(Article, pk=article_id)
    
    if request.method == "POST":
        selected_text = request.POST.get("selected_text")
        note_text = request.POST.get("note_text")

        if not note_text:
            return render(request, "annotation/notes.html", {
                "article": article,
                "error_message": "You didn't enter any note text.",
            })

        # Create a new note
        Note.objects.create(
            article=article,
            selected_text=selected_text or "",
            note_text=note_text
        )

        return redirect("detail", article_id=article.id)  # Adjust name as needed
    return render(request, "annotation/notes.html", {
        "article": article,
    })
    
    # if request.method == 'POST':
    #     form = NoteForm(request.POST)
    #     if form.is_valid():
    #         note = form.save(commit=False)
    #         note.article = article  # Set the related article
    #         note.save()
    #         return redirect('article_detail', article_id=article.id)  # Or any page you prefer
    # else:
    #     form = NoteForm()

    # return render(request, 'add_note.html', {'form': form, 'article': article})
