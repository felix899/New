from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.package_detail, name='package_detail'),
    # 其他URL模式...
]