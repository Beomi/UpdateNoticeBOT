import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()

from django.conf import settings
import telegram


from webchecker.models import ParsedData
from webchecker.web_parser import _get_contents

news = _get_contents(settings.SNUE_ID, settings.SNUE_PW)
latest_db_data = ParsedData.objects.last()

bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)   #bot을 선언합니다.

def push_telegram():
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