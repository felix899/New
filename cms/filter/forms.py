from django import forms
from sns.models import Package, RoomCategory
from django.contrib.postgres.forms import RangeWidget

class FilterForm(forms.Form):
    price_range = forms.DecimalField(min_value=0, max_value=1000000, required=False)
    room_category = forms.ModelChoiceField(queryset=RoomCategory.objects.all(), required=False)
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)