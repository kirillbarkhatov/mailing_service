from django import forms
from .models import Mailing

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        widgets = {
            'recipients': forms.CheckboxSelectMultiple(),
        }