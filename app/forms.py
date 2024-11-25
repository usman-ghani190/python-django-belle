
from django import forms
from .models import OrderItem, ProductQueryAsk, Review
from django.utils.translation import gettext_lazy as _


class OrderItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


# class ProductQeuryAskForm(forms.ModelForm):
#     class Meta:
#         model= ProductQueryAsk
#         fields='__all__'
#         labels= {'name': _(''),
#                  'email': _(''),
#                  'phone_number': _(''),
#                  'message': _('')}

        
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.fields['name'].widget.attrs['placeholder'] = 'Name'
#             self.fields['email'].widget.attrs['placeholder'] = 'Email'
#             self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
#             # self.fields['message'].widget.attrs.update({
#             # 'placeholder': 'Message',
#             # 'rows': 10,  # Add the rows attribute here
#             self.fields['message'].widget.attrs['placeholder'] = 'Message'

class ProductQueryAskForm(forms.ModelForm):
    class Meta:
        model = ProductQueryAsk
        fields = ['name', 'email', 'phone_number', 'message']
        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'phone_number': _('Phone Number'),
            'message': _('Message'),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Name', 'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email', 'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Phone Number', 'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Message', 'class': 'form-control', 'rows': 10
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'rating', 'review_title', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'john.smith@example.com'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review_title': forms.TextInput(attrs={'placeholder': 'Give your review a title'}),
            'comment': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your review here'}),
        }
        
        
            
    
        
                 