import email
from django import forms
from .models import OrderItem, Product
from django.utils.translation import gettext_lazy as _

class OrderItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class ProductQeuryAskForm(forms.ModelForm):
    class Meta:
        model= Product
        fields='__all__'
        labels= {'name': _(''),
                 'email': _(''),
                 'phone_number': _(''),
                 'message': _(''),
        }

        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['name'].widget.attrs['placeholder'] = 'Name'
            self.fields['email'].widget.attrs['placeholder'] = 'Email'
            self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
            self.fields['message'].widget.attrs['placeholder'] = 'Messsage'
        
                 