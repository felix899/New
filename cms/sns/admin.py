from django import forms
from django.contrib import admin
from django.contrib.postgres.fields import DateRangeField
from psycopg2.extras import DateRange
from django.forms.widgets import SelectDateWidget
from .models import Package, PackageType, RoomCategory, Room
from filer.models import Folder
from filer.fields.folder import FilerFolderField

class PackageAdminForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_folder'].widget = forms.Select(choices=self.get_folder_choices())
        self.fields['video_folder'].widget = forms.Select(choices=self.get_folder_choices())
        self.fields['media_folder'].widget = forms.Select(choices=self.get_folder_choices())

    def get_folder_choices(self):
        folders = Folder.objects.all()
        choices = [('', '---------')]
        for folder in folders:
            folder_path = self.get_folder_path(folder)
            choices.append((folder.id, folder_path))
        return choices

    def get_folder_path(self, folder):
        path = folder.name
        parent = folder.parent
        while parent:
            path = f"{parent.name}/{path}"
            parent = parent.parent
        return path

class RoomAdminForm(forms.ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget(), required=False)
    end_date = forms.DateField(widget=SelectDateWidget(), required=False)

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['valid_period']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.valid_period:
            self.fields['start_date'].initial = self.instance.valid_period.lower
            self.fields['end_date'].initial = self.instance.valid_period.upper

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("結束日期必須晚於開始日期。")
            cleaned_data['valid_period'] = DateRange(start_date, end_date)
        elif start_date or end_date:
            raise forms.ValidationError("請同時提供開始日期和結束日期，或者都不提供。")
        else:
            cleaned_data['valid_period'] = None

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.valid_period = self.cleaned_data.get('valid_period')
        if commit:
            instance.save()
        return instance

class RoomInline(admin.TabularInline):
    form = RoomAdminForm
    model = Room
    extra = 1
    min_num = 1
    max_num = 10
    fields = ('name', 'category', 'price', 'extended_price', 'start_date', 'end_date', 'notes')
    verbose_name = "Room"
    verbose_name_plural = "Rooms"

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    form = PackageAdminForm
    list_display = ('name', 'package_type', 'cover_photo', 'icon', 'image_folder', 'media_folder', 'video_folder')
    list_filter = ('package_type',)
    inlines = [RoomInline]

@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    list_display = ('name', 'package', 'category', 'price', 'extended_price', 'get_valid_period')
    list_filter = ('package', 'category')

    def get_valid_period(self, obj):
        if obj.valid_period:
            return f"{obj.valid_period.lower} to {obj.valid_period.upper}"
        return "Not set"
    get_valid_period.short_description = 'Valid Period'