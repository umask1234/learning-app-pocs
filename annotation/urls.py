from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# from .views import NoteViewSet
# from .views import NotesView


# router = DefaultRouter()
# router.register(r'notes', NoteViewSet)



urlpatterns = [
    path("", views.index, name="article-index"),
    path("<int:article_id>/", views.detail, name="detail"),
    path('<int:article_id>/notes/', views.notes, name='add_note'), 
    path('<int:article_id>/notes/<int:note_id>/edit/', views.notes, name='edit_note'),
    path('<int:article_id>/notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('articles/', views.articles, name='add_article'),
    path('articles/<int:article_id>/edit/', views.articles, name='edit_article'),
]