from django import forms
from .models import OrderItem

class OrderItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']