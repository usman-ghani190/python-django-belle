
from django import forms
from .models import Checkout, OrderItem, Payment, ProductQueryAsk, Register, Review
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    # Meta class to define the model and fields to include
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # Optional: Customize the password confirmation logic if needed
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password and confirm_password and password != confirm_password:
            self.add_error('password2', "Passwords do not match")
        
        return cleaned_data

    # Optional: Ensure email is unique (recommended)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


# class RegisterForm(UserCreationForm):
#     first_name = forms.CharField(max_length=100, required=True)
#     last_name = forms.CharField(max_length=100, required=True)
#     email = forms.EmailField(required=True)

#     # Meta class to define the model and fields to include
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

#     # Optional: Customize the password confirmation logic if needed
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password1")
#         confirm_password = cleaned_data.get("password2")

#         if password != confirm_password:
#             self.add_error('password2', "Passwords do not match")
        
#         return cleaned_data
    

# class LoginForm(forms.Form):
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'id': 'CustomerEmail',
#             'placeholder': 'Enter your email',
#         })
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'id': 'CustomerPassword',
#             'placeholder': 'Enter your password',
#         })
#     )


#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         password = cleaned_data.get('password')

#         if email and password:
#             user = authenticate(username=email, password=password)
#             if not user:
#                 raise forms.ValidationError("Invalid email or password")
#             elif not user.is_active:
#                 raise forms.ValidationError("This account is inactive.")
#         return cleaned_data

                 