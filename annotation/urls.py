from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# from .views import NoteViewSet
# from .views import NotesView


# router = DefaultRouter()
# router.register(r'notes', NoteViewSet)



urlpatterns = [
    path("", views.index, name="index"),
    path("<int:article_id>/", views.detail, name="detail"),
    # path('note/', include(router.urls))
    # path('<int:article_id>/notes/', NotesView.as_view(), name='notes')
    path('<int:article_id>/notes/', views.notes, name='add_note')
]