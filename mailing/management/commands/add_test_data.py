from django.core.management import call_command
from django.core.management.base import BaseCommand

from mailing.models import Mailing, MailingAttempt, Message, Recipient
from users.models import CustomUser


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

        # создаем тестовых пользователей
        call_command("create_test_users")

        # распределяем владельцев
        recipients = Recipient.objects.all()
        messages = Message.objects.all()
        mailing = Mailing.objects.all()
        owner = CustomUser.objects.get(email="test1@test1.ru")
        recipients.update(owner=owner)
        messages.update(owner=owner)
        mailing.update(owner=owner)

        self.stdout.write(
            self.style.SUCCESS(
                f"Владельцем всех получателей, рассылок и сообщений, загруженных из фикстур, назначен пользователь {owner.email}"
            )
        )

        other_owner = CustomUser.objects.get(email="test2@test2.ru")
        Recipient.objects.create(
            email="qwerty@asdfg.ru",
            full_name="qwerty asdfg",
            comment="Тестовый получатель для пользователя test2@test2.ru",
            owner=other_owner,
        )
        Message.objects.create(
            title="Смотри! Это тема сообщения! test2@test2.ru",
            message="Смотри! Это само сообщение! test2@test2.ru",
            owner=other_owner,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Для пользователя {other_owner.email} добавлены получатель и сообщение для нужд тестирования"
            )
        )
