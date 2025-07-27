from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Book
from django.db.models import Q
from django.http import HttpResponse
import operator

# Create your views here.

def index(request):
    users = User.objects.all()
    books = Book.objects.all()
    return render(request, 'bookshelf/index.html', {'users': users, 'books': books})

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
            user.name = name
            user.age = age
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
            book.name = name
            book.price = price
            book.save()
        return redirect('index')
    return render(request, 'bookshelf/books.html', {
        'books': Book.objects.all(), 
        "name": book.name if book else "", 
        "price": book.price if book else ""
    })

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('index')

def get_queried_params(table, key, constraint):
    print("table: ", table, ", key: ", key, " constraint: ", constraint)

    # Define supported operators
    comparative_operators = [
        ('==', "exact"),          # list ordered so that >= is before >, etc., so >= gets detected. 
        ('>=', "gte"),
        ('<=', "lte"),
        ('>', "gt"),
        ('<', "lt"),
    ]

    # Parse the constraint
    for op_str, op_func in comparative_operators:
        if op_str in constraint:
            try:
                if (key != "name" and key != "age" and key != "price"):
                    raise Exception("Invalid key.")
                value = constraint.split(op_str)[1].strip()
                if (key == "age"):
                    value = int(value)
                elif (key == "price"):
                    value = float(value)
                q_obj = Q(**{f"{key}__{op_func}": value})
                if (table == "user"):
                    return User.objects.filter(q_obj)
                elif (table == "book"):
                    return Book.objects.filter(q_obj)
            except Exception as e:
                print("Error parsing constraint:", e)
                return User.objects.none()

    # Fallback: no valid operator
    return User.objects.none()

def query_view(request):
    table = request.GET.get('table')
    key = request.GET.get('key')
    constraint = request.GET.get('constraint')

    results = get_queried_params(table, key, constraint)
    
    return render(request, 'bookshelf/query.html', {'results': results, 'table': table})
