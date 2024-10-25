from django import forms
from .models import Mailing, Recipient

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        widgets = {
            'recipients': forms.CheckboxSelectMultiple(),
        }


class RecipientForm(forms.ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = Recipient
        # Включаем все поля с модели в форму
        fields = "__all__"
