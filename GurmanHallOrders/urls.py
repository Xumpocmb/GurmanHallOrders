from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_home.urls')),
    path('catalog/', include('app_catalog.urls')),
    path('user/', include('app_user.urls')),
    path('order/', include('app_order.urls')),
]
