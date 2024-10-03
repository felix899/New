from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from sns import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filter/', include('filter.urls')),
    path('', include('sns.urls')),
    path('package/<int:pk>/', views.package_detail, name='package_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)