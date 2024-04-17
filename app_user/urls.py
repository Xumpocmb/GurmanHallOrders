from django.urls import path
from app_user.views import register_view, login_view, logout_view, add_to_cart_view, cart_view, remove_from_cart_view

app_name = 'app_user'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-to-cart/<int:item_id>/<int:param_id>/', add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', remove_from_cart_view, name='remove_from_cart'),
    path('cart/', cart_view, name='cart'),
]
