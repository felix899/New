from django.shortcuts import render, get_object_or_404
from .models import Package

def index(request):
    return render(request, 'sns/index.html')

def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, 'sns/package_detail.html', {'package': package})