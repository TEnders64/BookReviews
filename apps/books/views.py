from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Book, User, Review

# Create your views here.
def index(request):
    return render(request, 'books/index.html')

def login(request):
    if request.method == "POST":
        result = User.userMgr.login(
            email       =   request.POST['email'],
            password    =   request.POST['password']
        )
        if result[0]:
            request.session['user_id'] = result[1].id
            request.session['user_name'] = result[1].name
            return redirect(reverse('books_index'))
        else:
            for error in result[1]:
                messages.add_message(request, messages.INFO, result[1][error])
            return redirect(reverse('login_reg'))
    else:
        return redirect(reverse('login_reg'))

def register(request):
    if request.method == "POST":
        result = User.userMgr.register(
            name        =   request.POST['name'],
            alias       =   request.POST['alias'],
            email       =   request.POST['email'],
            password    =   request.POST['password'],
            c_password  =   request.POST['c_password']
        )
        if result[0]:
            request.session['user_id'] = result[1].id
            request.session['user_name'] = result[1].name
            return redirect(reverse('books_index'))
        else:
            for error in result[1]:
                messages.add_message(request, messages.INFO, result[1][error])
            return redirect(reverse('login_reg'))
    else:
        return redirect(reverse('login_reg'))

def logout(request):
    request.session.pop('user_id')
    request.session.pop('user_name')
    return redirect(reverse('login_reg'))

def show_user(request, user_id):
    user = User.userMgr.get(id=user_id)
    books = user.book_set.all()
    return render(request, 'books/show_user.html', {'user': user, 'books': books})

def books(request):
    reviews = Review.objects.order_by('-created_at').all()[:3]
    return render(request, 'books/books.html', {'reviews': reviews})

def show_book(request, book_id):
    book = Book.bookMgr.get(id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'books/show_book.html', {'book': book, 'reviews': reviews})

def add_book(request):
    authors = Book.bookMgr.distinct().values('author')
    return render(request, 'books/add_book.html', {'authors': authors})

def create_book(request):
    if request.method == "POST":
        result = Book.bookMgr.add(
            title    =   request.POST['title'],
            author   =   request.POST['author'],
            review   =   request.POST['review'],
            rating   =   int(request.POST['rating']),
            user     =   request.session['user_id']
        )
        if result[0]:
            return redirect(reverse('books_show', args=[result[1].id]))
        else:
            for error in result[1]:
                messages.add_message(request, messages.INFO, result[1][error])
            return redirect(reverse('books_add'))
    else:
        return redirect(reverse('books_add'))

def add_book_review(request, book_id):
    if request.method == "POST":
        result = Book.bookMgr.add_review(
            review = request.POST['review'],
            rating = int(request.POST['rating']),
            book   = book_id,
            user   = request.session['user_id']
        )
        if result[0]:
            return redirect(reverse('books_show', args=[book_id]))
        else:
            for error in result[1]:
                messages.add_message(request, messages.INFO, result[1][error])
            return redirect(reverse('books_show', args=[book_id]))

    else:
        return redirect(reverse('books_show', args=[book_id]))

def delete_review(request, review_id):
    pass
