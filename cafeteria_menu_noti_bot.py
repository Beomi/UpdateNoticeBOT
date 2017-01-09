import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()
from django.conf import settings

from webchecker.models import CafeMenuInfo, CafeMealTime, Guest
import telegram

bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
