from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Library, Book, IssuedBook
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# django rest framework imports
from . serializers import BookSerializer, IssueBookSerializer, LibrarySerializer
from rest_framework.decorators import api_view

# Create your views here.

@login_required
@api_view(['Get'])
def library(request):
    lib = Library.objects.filter(user=request.user)
    serializer = LibrarySerializer(lib, many=True)
    return render(request, 'library.html', {'lib':serializer.data})
# def library(request):
#     lib = Library.objects.filter(user=request.user).order_by('-created_at').reverse
#     return render(request, 'library.html', {'lib':lib})

@login_required
@api_view(['Get','Post'])
def lib_create(request):
    if request.method == "POST":
        name = request.POST.get("library_name")
        address = request.POST.get("lib_address")

        Library.objects.create(
            user = request.user,
            library_name = name,
            lib_address = address
        )
        return redirect('library')
    return render(request, 'lib_create.html')

@login_required
@api_view(['Get','Post'])
def rename_library(request, lib_id):
    lib = get_object_or_404(Library, pk=lib_id, user = request.user)
    if request.method == 'POST':
        name = request.POST.get("library_name")
        address = request.POST.get("lib_address")

        Library.objects.filter(id=lib_id).update(
            library_name = name,
            lib_address = address
        )

        return redirect('library')
    old_name = lib.library_name
    old_address = lib.lib_address
    return render(request, 'lib_create.html', {'lib_id':lib_id, 'old_name':old_name, 'old_address': old_address})
        
@login_required
@api_view(['Get','Post'])
def lib_del(request, lib_id):
    lib = get_object_or_404(Library, pk=lib_id, user = request.user)
    if request.method == 'POST':
        lib.delete()
        return redirect('library')
    return render(request, 'lib_delete.html', {'lib':lib})

# Authantication views
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

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#             login(request, user)
#             return redirect('library')
#     else:
#         # initial_data = ['username': "", 'password1': "", 'password2': ""]
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})

def logged_out(request):
    logout(request)
    return render(request, 'registration/logout.html')

# Django rest framework views
@login_required
@api_view(['GET'])
def open(request, lib_id):
    books = Book.objects.filter(library=lib_id)
    serializer = BookSerializer(books, many=True)

    return render(request, 'open.html', { 'books': serializer.data, 'lib_id': lib_id })

@login_required
@api_view(['Get','Post'])
def update(request, book_id, lib_id):
    book_ins = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        copies = request.POST.get("copies")
        price = request.POST.get("price")

        library_obj = Library.objects.get(id=lib_id)
        Book.objects.filter(id=book_id).update(
            title=title,
            author=author,
            copies = copies,
            price=price,
            library=library_obj
        )

        return redirect('open', lib_id)
    return render(request, "add_book.html", {'lib_id': lib_id, 'book_ins': book_ins})

@login_required
@api_view(['Get'])
def issued_books(request, lib_id):
    issued_books = IssuedBook.objects.filter(library=lib_id)
    serializer = IssueBookSerializer(issued_books, many=True)
    return render(request, 'issued_books.html', { 'issued_books': serializer.data, 'lib_id': lib_id })

@login_required
@api_view(['Get','Post'])
def add_book(request, lib_id):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        copies = request.POST.get("copies")
        price = request.POST.get("price")

        library_obj = Library.objects.get(id=lib_id)

        Book.objects.create(
            title=title,
            author=author,
            copies = copies,
            price=price,
            library=library_obj
        )

        return redirect('open', lib_id)
    return render(request, "add_book.html", {'lib_id': lib_id})

@login_required
@api_view(['Get','Post'])
def issue_book(request, book_id, lib_id):
    book_obj = get_object_or_404(Book, id=book_id)
    cur_copies = book_obj.copies
    lib_obj = get_object_or_404(Library, pk=lib_id)
    
    if request.method == "POST":
        issuer_name = request.POST.get("issuer_name")
        copy = int(request.POST.get('copies'))

        if (cur_copies - copy) < 0:
            return HttpResponse("That much copies are not available!")
        
        if (cur_copies - copy) == 0:
            Book.objects.filter(id=book_obj.id).update(
                available = False
            )

        if copy < 1:
            return HttpResponse("Copies cant be 0 or negative!")
        
        Book.objects.filter(id=book_obj.id).update(
            copies = cur_copies - copy
        )

        IssuedBook.objects.create(
            library = lib_obj,
            book = book_obj,
            issuer = issuer_name,
            copies = copy
        )


        return redirect('open', lib_id)
    return render(request, "issue_book.html", {"lib_id": lib_id})

@login_required
@api_view(['Get'])
def remove(request, book_id, lib_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('open', lib_id)

@login_required
@api_view(['Get','Post'])
def update_issued_book(request, book_id, lib_id):
    book_ins = get_object_or_404(IssuedBook, pk=book_id)
    if request.method == 'POST':
        issuer_name = request.POST.get("issuer_name")
        IssuedBook.objects.filter(id=book_id).update(
            issuer = issuer_name
        )

        return redirect('issued_books', lib_id)
    issuer_name = book_ins.issuer
    return render(request, "issue_book.html", {'lib_id': lib_id, 'book_ins': issuer_name})   

@login_required
@api_view(['Get','Post'])
def return_book(request, book_id, lib_id):
    issue_book_obj = get_object_or_404(IssuedBook, pk=book_id)

    if request.method == 'POST':
        i_copies = int(request.POST.get('copies'))

        if i_copies <= issue_book_obj.copies:
            book_obj = get_object_or_404(Book.objects.filter(id=issue_book_obj.book.id))
            print(issue_book_obj.book)
            b_copies = book_obj.copies

            Book.objects.filter(id=book_obj.id).update(
                copies =  + b_copies + i_copies,
                available = True
            )

            IssuedBook.objects.filter(id=book_id).update(
                copies = issue_book_obj.copies - i_copies
            )

            if issue_book_obj.copies - i_copies == 0:
                IssuedBook.objects.filter(id=issue_book_obj.id).delete()
        else:
            print(issue_book_obj.copies)
            return HttpResponse("Returning more books than issued")

        return redirect('issued_books', lib_id)
    return render(request, 'return.html', {'lib_id': lib_id})