from django.urls import path
from . import views

urlpatterns = [
    path('', views.filter_page, name='filter_page'),
    path('api/', views.filter_packages, name='filter_packages'),
]