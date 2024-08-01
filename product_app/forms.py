from django import forms
from .models import ProductReview

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
