from django import forms
from .models import CounselingSession
from accounts.models import CustomUser

class BookSessionForm(forms.ModelForm):
    counselor = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='counselor'),
        empty_label="Select a Counselor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CounselingSession
        fields = ['counselor', 'date', 'preferred_time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'preferred_time': forms.TextInput(attrs={'placeholder': 'e.g. 10:00 AM', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class UpdateSessionForm(forms.ModelForm):
    class Meta:
        model = CounselingSession
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
