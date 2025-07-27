from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_user/', views.users, name='add_user'),
    path('edit_user/<int:user_id>/', views.users, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add_book/', views.books, name='add_book'),
    path('edit_book/<int:book_id>/', views.books, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('query/', views.query_view, name='query'),
]