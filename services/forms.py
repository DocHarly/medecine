from django import forms

from .models import Services

class ServicesForm(forms.ModelForm):

    class Meta:
        model = Services
        fields = ['title', 'price', 'text',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }