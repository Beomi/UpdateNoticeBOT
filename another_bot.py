import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()

from django.conf import settings
from webchecker.models import ParsedData


from telegram.ext import Updater, CommandHandler

def start(bot, update):
    latest_db_data = ParsedData.objects.all().order_by('py_date').last()
    update.message.reply_text('안녕하세요,\nSNUE알림봇을 추가해주셔서 감사합니다.\n이시간 이후로 새로운 공지사항이 오는 경우 즉시 알려드리겠습니다 :)')
    update.message.reply_text('현재 가장 최근 공지는 {}일의 공지입니다.'.format(
            latest_db_data.date
        ))
    update.message.reply_text("{}\n{}\n{}".format(
            latest_db_data.title, 
            latest_db_data.date, 
            latest_db_data.url
        ))

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

updater = Updater(settings.TELEGRAM_TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()