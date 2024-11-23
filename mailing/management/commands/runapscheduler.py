import logging

from django.conf import settings
from django.db.models import Q

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from django.utils.timezone import now
from config.settings import DEFAULT_FROM_EMAIL
from mailing.models import Mailing, MailingAttempt
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_mailing():
    """Функция для отправки рассылок."""

    logger.info("Запуск задачи отправки рассылок...")
    mailings = Mailing.objects.filter(
        Q(status=Mailing.CREATED) | Q(status=Mailing.RUNNING),  # Логическое "ИЛИ"
        first_send_at__lte=now(),
        finish_send_at__gte=now()
    )

    for mailing in mailings:
        recipients = mailing.recipients.all()
        for recipient in recipients:
            try:
                # Отправка письма
                send_mail(
                    subject=mailing.message,
                    message=mailing.message.message,
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                )
                status = MailingAttempt.SUCCESS
                response = f"{recipient.email}: Успешно отправлено"

            except Exception as e:
                logger.error(f"Ошибка при отправке: {e}")
                status = MailingAttempt.FAILURE
                response = f"{recipient.email}: Ошибка: {str(e)}"

            # Создание записи о попытке
            MailingAttempt.objects.create(
                attempted_at=now(),
                status=status,
                mail_server_response=response,
                mailing=mailing,
            )

        # Обновление статуса рассылки
        mailing.status = Mailing.RUNNING
        mailing.save()
    logger.info("Задача отправки рассылок завершена.")


def auto_completing_mailing():
    """Проверка статусов рассылок и их автоматическое закрытие, если время истекло."""

    logger.info("Запуск задачи обновления статуса рассылок...")
    mailings = Mailing.objects.filter(
        Q(status=Mailing.CREATED) | Q(status=Mailing.RUNNING),  # Логическое "ИЛИ"
        finish_send_at__lte=now()
    )

    for mailing in mailings:

        # Обновление статуса рассылки
        mailing.status = Mailing.COMPLETED
        mailing.save()
    logger.info("Задача обновления статуса рассылок завершена.")


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Удаляет записи выполненных задач APScheduler старше max_age.
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_mailing,
            trigger=CronTrigger(minute="*/1"),  # Выполнять каждые 1 минуту
            id="send_mailing_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена задача 'send_mailing_job'.")

        scheduler.add_job(
            auto_completing_mailing,
            trigger=CronTrigger(minute="*/1"),  # Выполнять каждые 1 минуту
            id="auto_completing_mailing_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена задача 'auto_completing_mailing_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Добавлена еженедельная задача 'delete_old_job_executions'."
        )

        try:
            logger.info("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик успешно остановлен.")
