from django import forms
from .models import AnonymousPost

class AnonymousPostForm(forms.ModelForm):
    class Meta:
        model = AnonymousPost
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share what is on your mind. Your identity is completely anonymous.'
            })
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = AnonymousPost
        fields = ['response', 'is_resolved']
        widgets = {
            'response': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_resolved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
