from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Book
from django.db.models import Q

# Create your views here.

def index(request):
    users = User.objects.all()
    books = Book.objects.all()
    return render(request, 'bookshelf/index.html', {'users': users, 'books': books})

def query_view(request):
    table = request.GET.get('table')
    key = request.GET.get('key')
    constraint = request.GET.get('constraint')

    results = []
    if table == 'user':
        results = User.objects.filter(eval(f"Q({key} {constraint})"))       # needed - input sanitization
    elif table == 'book':
        results = Book.objects.filter(eval(f"Q({key} {constraint})"))
    
    return render(request, 'bookshelf/query_result.html', {'results': results, 'table': table})

def users(request, user_id=None):
    user = None if user_id is None else get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        liked_books = request.POST.getlist('liked_books')
        if user is None:    # creating a new user
            user = User.objects.create(name=name, age=age)
            user.liked_books.set(Book.objects.filter(id__in=liked_books))
        else:               # editing a preexisting user
            user.liked_books.set(Book.objects.filter(id__in=liked_books))
            user.save()
        return redirect('index')
    return render(request, 'bookshelf/users.html', {
        'books': Book.objects.all(), 
        "name": user.name if user else "", 
        "age": user.age if user else "", 
        "liked": user.liked_books.all() if user else None
    })

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('index')

def books(request, book_id=None):
    book = None if book_id is None else get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        if book is None:    # creating a new book
            book = Book.objects.create(name=name, price=price)
        else:               # editing a preexisting book
            user.save()
        return redirect('index')
    return render(request, 'bookshelf/books.html', {
        'books': Book.objects.all(), 
        "name": book.name if book else "", 
        "price": book.price if book else ""
    })
