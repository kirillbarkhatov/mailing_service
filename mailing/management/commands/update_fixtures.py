from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Обновление данных в фикстурах"

    def handle(self, *args, **kwargs):

        pass

        # ОПАСНО! НАРУШАЕТСЯ ЦЕЛОСТНОСТЬ И ПОТОМ НЕ ПОДГРУЗИТЬ - КАКИЕ-ТО ПРОБЛЕМЫ С ВЛАДЕЛЬЦАМИ И ИХ id
        # call_command('dumpdata', 'mailing.Mailing', output='mailing_fixture.json', indent=4)
        # call_command('dumpdata', 'mailing.MailingAttempt', output='mailing_attempts_fixture.json', indent=4)
        # call_command('dumpdata', 'mailing.Message', output='messages_fixture.json', indent=4)
        # call_command('dumpdata', 'mailing.Recipient', output='recipients_fixture.json', indent=4)
        # self.stdout.write(
        #     self.style.SUCCESS("Фикстуры созданы")
        # )
