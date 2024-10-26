from django.contrib import admin

from .forms import MailingForm
from .models import Mailing, MailingAttempt, Message, Recipient

# Register your models here.

# стандартное отображение через метод __str__
admin.site.register(Recipient)
admin.site.register(Message)
# admin.site.register(Mailing)
admin.site.register(MailingAttempt)


# Кастомное отображение в админке
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):

    form = MailingForm

    list_display = (
        "id",
        "first_send_at",
        "finish_send_at",
        "status",
        "message",
        "get_recipients",  # специальное отображение ManyToManyField
    )  # вывод колонок

    # search_fields = (
    #     "title",
    #     "content",
    # )  # поиск по указанному полю/полям

    def short_content(self, obj):
        # Обрезаем текст до 50 символов и добавляем '...' если он длиннее
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    short_content.short_description = "message"  # Название колонки в админке

    # специальное отображение ManyToManyField
    def get_recipients(self, obj):
        return ", ".join([recipient.email for recipient in obj.recipients.all()])

    get_recipients.short_description = "recipients"  # Название колонки в админке
