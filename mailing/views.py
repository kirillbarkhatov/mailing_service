from datetime import datetime
from lib2to3.fixes.fix_input import context

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from mailing.models import Recipient, Message, Mailing, MailingAttempt
from mailing.forms import RecipientForm, MessageForm, MailingForm

# Create your views here.

class IndexView(TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_attempt = MailingAttempt.objects.all()
        attempt_count = mailing_attempt.count()
        attempt_success_count = mailing_attempt.filter(status="success").count()
        attempt_failure_count = mailing_attempt.filter(status="failure").count()
        mailing_count = Mailing.objects.count()
        mailing_running_count = Mailing.objects.filter(status="running").count()
        recipient_count = Recipient.objects.count()
        context["object_list"] = mailing_attempt
        context["attempt_count"] = attempt_count
        context["attempt_success_count"] = attempt_success_count
        context["attempt_failure_count"] = attempt_failure_count
        context["mailing_count"] = mailing_count
        context["mailing_running_count"] = mailing_running_count
        context["recipient_count"] = recipient_count
        return context


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

        from_email = "barchatovkirill@mail.ru"
        recipient_list = [recipient.email for recipient in self.object.recipients.all()]  # Укажите адреса получателей

        # Отправка письма
        # responses = {}

        for recipient in recipient_list:
            try:
                send_mail(subject, message, from_email, [recipient])
                response = f"{recipient}: Успешно отправлено"
                MailingAttempt.objects.create(attempted_at=timezone.now(), status="success", mail_server_response=response, mailing= self.object)
                # responses[recipient] = "Успешно отправлено"
            except Exception as e:
                response = f"{recipient}: Ошибка: {str(e)}"
                # responses[recipient] = f"Ошибка: {str(e)}"
                MailingAttempt.objects.create(attempted_at=datetime.now(), status="failure",
                                              mail_server_response=response, mailing=self.object)

        # Вывод ответов для проверки
        # for recipient, response in responses.items():
        #     print(f"{recipient}: {response}")

        # Перенаправление после отправки письма
        return redirect('mailing:mailing_list')  # Укажите нужный URL для перенаправления


# Контроллер для модели "Попытка рассылки"
class MailingAttemptListView(ListView):
    model = MailingAttempt
