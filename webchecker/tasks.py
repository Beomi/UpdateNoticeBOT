from django.conf import settings

from celery import shared_task
import telegram


bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)   #bot을 선언합니다.


@shared_task
def get_updates():
    updates = bot.getUpdates()
    for u in updates:
        print(u.message)

@shared_task
def some_parser():
    print('hello!')