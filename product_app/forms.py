from django import forms

from account_app.models import Address
from .models import ProductReview, OrderItem


class ProductReviewForm(forms.ModelForm):
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = ProductReview
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'نظر خود را بنویسید...',
                'class': 'form-textarea'
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-input'
            }),
        }

# forms.py


class ReplyForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'پاسخ خود را بنویسید...'}),
        }

class OrderItemUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']

class OrderItemDeleteForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'postal_code']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }