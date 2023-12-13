from django.shortcuts import render

def index(request):
    return render(request, 'gisil/index.html')

def entry_value(request):
    return render(request, 'gisil/gisil_values.html')