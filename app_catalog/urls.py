from django.urls import path
from app_catalog.views import catalog, category_detail

app_name = 'app_catalog'

urlpatterns = [
    path('', catalog, name='catalog'),
    path('<slug:slug>/', category_detail, name='category_detail'),
]
