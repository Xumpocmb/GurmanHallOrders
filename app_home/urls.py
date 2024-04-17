from django.urls import path
from app_home.views import index

app_name = 'app_home'

urlpatterns = [
    path('', index, name='home'),
]
