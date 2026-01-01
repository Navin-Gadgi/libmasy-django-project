from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Library, Book, IssuedBook
from .forms import LibraryForm, AddBookForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
# django rest framework imports
from . serializers import BookSerializer, IssueBookSerializer, LibrarySerializer,ReturnBookSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def newapp(request):
    return render(request, 'library.html')

@login_required
def library(request):
    lib = Library.objects.filter(user=request.user).order_by('-created_at').reverse
    return render(request, 'library.html', {'lib':lib})

@login_required
def lib_create(request):
    if request.method == "POST":
        name = request.POST.get("library_name")

        Library.objects.create(
            user = request.user,
            library_name = name
        )
        return redirect('library')
    return render(request, 'lib_create.html')

@login_required
def rename_library(request, lib_id):
    lib = get_object_or_404(Library, pk=lib_id, user = request.user)
    if request.method == 'POST':
        name = request.POST.get("library_name")

        Library.objects.filter(id=lib_id).update(
            library_name = name
        )

        return redirect('open', lib_id)
    old_name = lib.library_name
    return render(request, 'rename_library.html', {'lib_id':lib_id, 'old_name':old_name})
        
@login_required
def lib_del(request, lib_id):
    lib = get_object_or_404(Library, pk=lib_id, user = request.user)
    if request.method == 'POST':
        lib.delete()
        return redirect('library')
    return render(request, 'lib_delete.html', {'lib':lib})



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('library')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form':form})

def logged_out(request):
    logout(request)
    return render(request, 'registration/logout.html')

# Django rest framework views

@login_required
@api_view(['GET','POST'])
def open(request, lib_id):
    books = Book.objects.filter(library=lib_id)
    serializer = BookSerializer(books, many=True)

    return render(request, 'open.html', { 'books': serializer.data, 'lib_id': lib_id })

@login_required
def update(request, book_id, lib_id):
    book_ins = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        price = request.POST.get("price")

        library_obj = Library.objects.get(id=lib_id)
        Book.objects.filter(id=book_id).update(
            title=title,
            author=author,
            price=price,
            library=library_obj
        )

        return redirect('open', lib_id)
    return render(request, "update.html", {'lib_id': lib_id, 'book_ins': book_ins})

@login_required
def issued_books(request, lib_id):
    issued_books = IssuedBook.objects.filter(library=lib_id)
    serializer = IssueBookSerializer(issued_books, many=True)
    return render(request, 'issued_books.html', { 'issued_books': serializer.data, 'lib_id': lib_id })

@login_required
def add_book(request, lib_id):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        price = request.POST.get("price")

        library_obj = Library.objects.get(id=lib_id)

        Book.objects.create(
            title=title,
            author=author,
            price=price,
            library=library_obj
        )

        return redirect('open', lib_id)
    return render(request, "add_book.html", {'lib_id': lib_id})

@login_required
def issue_book(request, book_id, lib_id):
    book_obj = get_object_or_404(Book, id=book_id)
    lib_obj = get_object_or_404(Library, pk=lib_id)
    
    if request.method == "POST":
        issuer_name = request.POST.get("issuer_name")

        IssuedBook.objects.create(
            library = lib_obj,
            book = book_obj,
            issuer = issuer_name
        )

        Book.objects.filter(id=book_obj.id).update(
        available = False
        )

        return redirect('open', lib_id)
    return render(request, "issue_book.html", {"lib_id": lib_id})

@login_required
def remove(request, book_id, lib_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('open', lib_id)


@login_required
def return_book(request, book_id, lib_id):
    issue_book_obj = get_object_or_404(IssuedBook, pk=book_id)
    book_obj = get_object_or_404(Book.objects.filter(id=issue_book_obj.book.id))
    Book.objects.filter(id=book_obj.id).update(
        available = True
    )
    IssuedBook.objects.filter(id=book_id).delete()
    return redirect('issued_books', lib_id)