from django.conf import settings
from django.utils import timezone

from celery import shared_task
import telegram

from .web_parser import _get_contents
from .models import ParsedData

bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)   #bot을 선언합니다.


@shared_task
def get_updates():
    latest = bot.getUpdates()[-1]
    chat_id = latest.message.chat.id
    bot.sendMessage(chat_id=chat_id, text=latest.message.text)

@shared_task
def new_noti():
    bot.send_message(chat_id=settings.TEST_ID, text='progress...')
    news = _get_contents(settings.SNUE_ID, settings.SNUE_PW)
    latest_db_data = ParsedData.objects.last()
    if news[0].get('py_date') > latest_db_data.py_date:
        for n in news:
            title = n.get('title')
            date = n.get('date')
            py_date = n.get('py_date')
            url = n.get('url')

            if py_date > latest_db_data.py_date:
                PD = ParsedData(title=title, date=date, url=url, py_date=py_date)
                PD.save()
                bot.send_message(
                    chat_id=settings.TEST_ID,
                    text="{}\n{}\n{}".format(
                        title, date, url
                    )
                )
                return True
    return False

