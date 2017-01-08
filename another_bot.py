import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()

from django.conf import settings

from telegram.ext import Updater, CommandHandler

def start(bot, update):
    update.message.reply_text('Hello World!')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

updater = Updater(settings.TELEGRAM_TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()