from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'webtemps/home.html')

def about(request):
    return render(request, 'webtemps/about.html')

def contact(request):
    return render(request, 'webtemps/contact.html')