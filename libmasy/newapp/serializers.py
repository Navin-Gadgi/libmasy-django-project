from rest_framework import serializers
from .models import Book, IssuedBook, Library
from datetime import date

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
    
class ReturnBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssuedBook
        fields = []

    def update(self, instance):
        instance.is_returned = True
        instance.return_date = date.today()
        instance.save()

        book = instance.book
        book.available=True
        book.save()

        return instance