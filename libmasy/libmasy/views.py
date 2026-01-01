from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # var = request.GET.get('text', 'default')
    # print(var)
    return render(request, 'webtemps/home.html')

def about(request):
    return render(request, 'webtemps/about.html')

def contact(request):
    return render(request, 'webtemps/contact.html')