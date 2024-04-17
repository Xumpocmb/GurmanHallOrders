from django import forms
from app_order.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'phone',
                  'description', 'delivery_method', 'payment_method']
