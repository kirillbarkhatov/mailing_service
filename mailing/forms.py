from django import forms

from .models import Mailing, Message, Recipient


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"
        exclude = [
            "owner",
        ]
        widgets = {
            "recipients": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Получаем текущего пользователя
        super().__init__(*args, **kwargs)

        if user:
            # Фильтруем только те recipients, которые принадлежат текущему пользователю
            self.fields["recipients"].queryset = Recipient.objects.filter(owner=user)
            self.fields["message"].queryset = Message.objects.filter(owner=user)


class RecipientForm(forms.ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = Recipient
        # Включаем все поля с модели в форму
        fields = "__all__"
        exclude = [
            "owner",
        ]


class MessageForm(forms.ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = Message
        # Включаем все поля с модели в форму
        fields = "__all__"
        exclude = [
            "owner",
        ]
