from django import forms
from .models import Library, Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['library_name']

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','author','price']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        