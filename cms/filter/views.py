from django.shortcuts import render
from django.http import JsonResponse
from .forms import FilterForm
from sns.models import Package, Room

def filter_packages(request):
    form = FilterForm(request.GET)
    packages = Package.objects.all()

    if form.is_valid():
        price_range = form.cleaned_data.get('price_range')
        room_category = form.cleaned_data.get('room_category')
        check_in_date = form.cleaned_data.get('check_in_date')

        if price_range:
            packages = packages.filter(rooms__price__lte=price_range)
        if room_category:
            packages = packages.filter(rooms__category=room_category)
        if check_in_date:
            packages = packages.filter(rooms__valid_period__contains=check_in_date)

    packages = packages.distinct()

    data = [{
        'id': package.id,
        'name': package.name,
        'description': package.description,
    } for package in packages]

    return JsonResponse(data, safe=False)

def filter_page(request):
    form = FilterForm()
    return render(request, 'filter/filter_page.html', {'form': form})