from rest_framework import serializers
from .models import Book, IssuedBook, Library

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class IssueBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssuedBook
        fields = '__all__'
