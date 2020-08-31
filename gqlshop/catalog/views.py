from django.shortcuts import render
from django.http import HttpResponse


def index_view(request):
    return HttpResponse('<h2>ToDo!</h2>')