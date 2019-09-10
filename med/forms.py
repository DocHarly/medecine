from dal import autocomplete
from django import forms

from .models import Med, Clients

class MedForm(forms.ModelForm):

    class Meta:
        model = Med
        fields = ['client', 'service', 'text', ]
        widgets = {
            'client': autocomplete.ModelSelect2(url='med-autocomplete', attrs={'class' : 'form-control'}),
            'service': autocomplete.ModelSelect2(url='service-autocomplete', attrs={'class' : 'form-control'}),
            'text': forms.Textarea(attrs={'class' : 'form-control'})
        }