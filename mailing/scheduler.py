# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.executors.pool import ThreadPoolExecutor
# from django_apscheduler.jobstores import DjangoJobStore
# from .tasks import send_mailing
#
# def start_scheduler():
#     scheduler = BackgroundScheduler(executors={"default": ThreadPoolExecutor(10)})
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#
#     # Регистрация задачи
#     scheduler.add_job(
#         send_mailing,
#         "interval",
#         minutes=1,  # Интервал выполнения задачи
#         id="send_mailing_job",
#         replace_existing=True,
#     )
#
#     register_events(scheduler)
#     scheduler.start()
