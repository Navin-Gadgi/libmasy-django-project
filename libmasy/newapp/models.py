from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    library_name = models.CharField(max_length=20)
    lib_address = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.library_name[:10]}'

class Book(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    copies = models.PositiveIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class IssuedBook(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    issuer = models.CharField(max_length=20)
    copies = models.PositiveIntegerField(null=True, blank=True)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title 