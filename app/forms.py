
from django import forms
from .models import Checkout, OrderItem, Payment, ProductQueryAsk, Review
from django.utils.translation import gettext_lazy as _


class OrderItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


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
        
        
            
class CheckoutForm(forms.ModelForm):
    class Meta:
        model= Checkout
        fields= '__all__'
    


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['cardname', 'cardtype', 'cardno', 'cvv', 'exdate']

        widgets = {
            'cardname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Card Name',
                'id': 'input-cardname',
            }),
            'cardtype': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cardno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Credit Card Number',
                'id': 'input-cardno',
            }),
            'cvv': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Card Verification Number',
                'id': 'input-cvv',
            }),
            'exdate': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
    
        
                 