from django.core.management import call_command
from django.core.management.base import BaseCommand

from mailing.models import Mailing, MailingAttempt, Message, Recipient


class Command(BaseCommand):
    help = "Добавление данных из фикстур"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Recipient.objects.all().delete()
        Message.objects.all().delete()
        Mailing.objects.all().delete()
        MailingAttempt.objects.all().delete()

        # Добавляем данные из фикстур
        call_command("loaddata", "recipients_fixture.json", format="json")
        self.stdout.write(
            self.style.SUCCESS("Получатели рассылок загружены из фикстур успешно")
        )
        call_command("loaddata", "messages_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Сообщения загружены из фикстур успешно"))
        call_command("loaddata", "mailing_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Рассылки загружены из фикстур успешно"))
        call_command("loaddata", "mailing_attempts_fixture.json", format="json")
        self.stdout.write(
            self.style.SUCCESS("Попытки рассылок загружены из фикстур успешно")
        )
