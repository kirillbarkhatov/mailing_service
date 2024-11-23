from django.utils.timezone import now
from django_apscheduler.jobstores import register_events
from apscheduler.schedulers.background import BackgroundScheduler

from config.settings import DEFAULT_FROM_EMAIL
from .models import Mailing, MailingAttempt
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def send_mailing():
    """Функция для отправки рассылок."""
    mailings = Mailing.objects.filter(
        status=Mailing.CREATED, first_send_at__lte=now(), finish_send_at__gte=now()
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
        mailing.status = Mailing.COMPLETED
        mailing.save()
