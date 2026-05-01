from django import forms
from .models import WellnessResource

class WellnessResourceForm(forms.ModelForm):
    class Meta:
        model = WellnessResource
        fields = ['title', 'resource_type', 'content', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }
