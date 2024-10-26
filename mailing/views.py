from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from mailing.models import Recipient, Message, Mailing
from mailing.forms import RecipientForm, MessageForm, MailingForm

# Create your views here.

class IndexView(TemplateView):
    template_name = "mailing/index.html"


# CRUD для модели "Получатель рассылки"
class RecipientListView(ListView):
    model = Recipient


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")


# CRUD для модели "Сообщение"
class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


# CRUD для модели "Рассылки"
class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = Mailing.objects.prefetch_related('recipients')
        return queryset


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDetailView(DetailView):
    model = Mailing

    def get_queryset(self):
        queryset = Mailing.objects.prefetch_related('recipients')
        return queryset

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        # Получите данные, которые хотите отправить
        subject = self.object.message
        message = self.object.message.message

        print(subject)
        print(message)
        from_email = "barchatovkirill@mail.ru"
        recipient_list = [[recipient.email] for recipient in self.object.recipients.all()]  # Укажите адреса получателей
        print(recipient_list)

        # Отправка письма
        for recipient in recipient_list:
            send_mail(subject, message, from_email, recipient)

        # Перенаправление после отправки письма
        return redirect('mailing:mailing_list')  # Укажите нужный URL для перенаправления
