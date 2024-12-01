from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Mailing, MailingAttempt, Message, Recipient
from mailing.services import get_index_page_cache_data


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # получаем текущего пользователя и идем в кеш
        user = self.request.user
        context.update(get_index_page_cache_data(user))

        return context


# CRUD для модели "Получатель рассылки"
class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient

    def get_queryset(self):
        # фильтр данных по пользователю
        user = self.request.user
        if user.groups.filter(name="Менеджер").exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверка, состоит ли пользователь в группе "Менеджер"
        is_manager = self.request.user.groups.filter(name="Менеджер").exists()

        # Добавляем в контекст информацию, что пользователь является модератором
        context["is_manager"] = is_manager
        return context


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект
        obj = super().get_object()
        # Проверяем, является ли текущий пользователь владельцем объекта
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            "Вы не можете просматривать/изменять/удалять этот объект."
        )


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект
        obj = super().get_object()
        # Проверяем, является ли текущий пользователь владельцем объекта
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            "Вы не можете просматривать/изменять/удалять этот объект."
        )


# CRUD для модели "Сообщение"
class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        # фильтр данных по пользователю
        user = self.request.user
        if user.groups.filter(name="Менеджер").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверка, состоит ли пользователь в группе "Менеджер"
        is_manager = self.request.user.groups.filter(name="Менеджер").exists()

        # Добавляем в контекст информацию, что пользователь является модератором
        context["is_manager"] = is_manager
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект
        obj = super().get_object()
        # Проверяем, является ли текущий пользователь владельцем объекта
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            "Вы не можете просматривать/изменять/удалять этот объект."
        )


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект
        obj = super().get_object()
        # Проверяем, является ли текущий пользователь владельцем объекта
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            "Вы не можете просматривать/изменять/удалять этот объект."
        )


# CRUD для модели "Рассылки"
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):

        # фильтр данных по пользователю
        user = self.request.user
        if user.groups.filter(name="Менеджер").exists():
            return Mailing.objects.prefetch_related("recipients")
        return Mailing.objects.filter(owner=user.id).prefetch_related("recipients")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверка, состоит ли пользователь в группе "Менеджер"
        is_manager = self.request.user.groups.filter(name="Менеджер").exists()

        # Добавляем в контекст информацию, что пользователь является модератором
        context["is_manager"] = is_manager
        return context


class MailingStopView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        user = request.user

        # Проверка, состоит ли пользователь в группе "Менеджер"
        is_manager = user.groups.filter(name="Менеджер").exists()

        if is_manager or user == mailing.owner:
            # Логика снятия с публикации
            mailing.status = "completed"
            mailing.save()

            return redirect("mailing:mailing_list")
        return HttpResponseForbidden("У вас нет прав для отключения рассылки")


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Передаем текущего пользователя
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект
        obj = super().get_object()
        # Проверяем, является ли текущий пользователь владельцем объекта
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            "Вы не можете просматривать/изменять/удалять этот объект."
        )


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект
        obj = super().get_object()
        # Проверяем, является ли текущий пользователь владельцем объекта
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            "Вы не можете просматривать/изменять/удалять этот объект."
        )


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_queryset(self):
        queryset = Mailing.objects.prefetch_related("recipients")
        return queryset

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект
        obj = super().get_object()
        # Проверяем, является ли текущий пользователь владельцем объекта
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            "Вы не можете просматривать/изменять/удалять этот объект."
        )

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        # Получите данные, которые хотите отправить
        subject = self.object.message
        message = self.object.message.message
        # self.object.status = "running"
        # self.object.save()
        from_email = "barchatovkirill@mail.ru"
        recipient_list = [
            recipient.email for recipient in self.object.recipients.all()
        ]  # Укажите адреса получателей

        # Отправка письма
        # responses = {}

        for recipient in recipient_list:
            try:
                send_mail(subject, message, from_email, [recipient])
                response = f"{recipient}: Успешно отправлено"
                MailingAttempt.objects.create(
                    attempted_at=timezone.now(),
                    status="success",
                    mail_server_response=response,
                    mailing=self.object,
                )
                # responses[recipient] = "Успешно отправлено"
            except Exception as e:
                response = f"{recipient}: Ошибка: {str(e)}"
                # responses[recipient] = f"Ошибка: {str(e)}"
                MailingAttempt.objects.create(
                    attempted_at=datetime.now(),
                    status="failure",
                    mail_server_response=response,
                    mailing=self.object,
                )

        # Вывод ответов для проверки
        # for recipient, response in responses.items():
        #     print(f"{recipient}: {response}")

        # Перенаправление после отправки письма
        return redirect(
            "mailing:mailing_list"
        )  # Укажите нужный URL для перенаправления


# Контроллер для модели "Попытка рассылки"
class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt

    def get_queryset(self):

        # фильтр данных по пользователю
        user = self.request.user
        if user.groups.filter(name="Менеджер").exists():
            return MailingAttempt.objects.all()
        return MailingAttempt.objects.filter(mailing__owner=user.id)
