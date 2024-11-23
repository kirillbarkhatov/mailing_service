from lib2to3.fixes.fix_input import context

from django.core.cache import cache

from .models import MailingAttempt, Mailing, Recipient, CustomUser


def get_index_page_cache_data(user: CustomUser) -> dict:
    """Функция возвращает кешированные данные для главной страницы"""

    # проверяем кеш, если есть - отдаем в контроллер
    context_from_cache = cache.get(f"index_page_data/{user.email}")
    if context_from_cache:
        return context_from_cache

    # если кеша не оказалось, получаем данные из БД, записываем в кеш и отдаем в контроллер
    context_update = {}
    if user.groups.filter(name="Менеджер").exists():
        mailing_attempt = MailingAttempt.objects.all()
        mailing = Mailing.objects.all()
        recipient = Recipient.objects.all()

    else:
        mailing_attempt = MailingAttempt.objects.filter(mailing__owner=user.id)
        mailing = Mailing.objects.filter(owner=user.id)
        recipient = Recipient.objects.filter(owner=user.id)

    attempt_count = mailing_attempt.count()
    attempt_success_count = mailing_attempt.filter(status="success").count()
    attempt_failure_count = mailing_attempt.filter(status="failure").count()
    mailing_count = mailing.count()
    mailing_running_count = mailing.filter(status="running").count()
    recipient_count = recipient.count()
    context_update["object_list"] = mailing_attempt
    context_update["attempt_count"] = attempt_count
    context_update["attempt_success_count"] = attempt_success_count
    context_update["attempt_failure_count"] = attempt_failure_count
    context_update["mailing_count"] = mailing_count
    context_update["mailing_running_count"] = mailing_running_count
    context_update["recipient_count"] = recipient_count
    cache.set(f"index_page_data/{user.email}", context_update, 5)
    return context_update

    #
    # mailing_attempt_list = cache.get(f"products/category/{category_id}")
    # if products:
    #     return products
    # products = Product.objects.filter(category_id=category_id, is_published=True)
    # cache.set(f"products/category/{category_id}", products, 60)
    # return products
