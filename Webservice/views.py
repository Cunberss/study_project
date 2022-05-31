from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


def function(request):
    if request.method == 'GET':
        return render(request, 'index.html')

def news(request):
    if request.method == 'GET':
        return render(request, 'news.html')