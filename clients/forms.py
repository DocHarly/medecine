from django import forms
import datetime
from .models import Clients

class ClientsForm(forms.ModelForm):

    class Meta:
        model = Clients
        fields = ['name', 'fam', 'date_birthday', 'med_card',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'fam': forms.TextInput(attrs={'class': 'form-control'}),
            'date_birthday': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control'}),
            'med_card': forms.Textarea(attrs={'class': 'form-control'}),
        }