import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()

from django.conf import settings
import telegram

from webchecker.models import ParsedData
from webchecker.models import Guest
from webchecker.web_parser import _get_contents

news = _get_contents(settings.SNUE_ID, settings.SNUE_PW)
latest_db_data = ParsedData.objects.all().order_by('py_date').last()

bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)   #bot을 선언합니다.

def push_telegram():
    if news[0].get('py_date') > latest_db_data.py_date:
        for n in reversed(news):
            title = n.get('title')
            date = n.get('date')
            py_date = n.get('py_date')
            url = n.get('url')

            if py_date > latest_db_data.py_date:
                PD = ParsedData(title=title, date=date, url=url, py_date=py_date)
                PD.save()
                for guest in Guest.objects.filter(options__name='notice'):
                    bot.send_message(
                        chat_id=guest.telegram_id,
                        text="{}\n{}\n{}".format(
                            title, date, url
                        )
                    )

if __name__=='__main__':
    push_telegram()
