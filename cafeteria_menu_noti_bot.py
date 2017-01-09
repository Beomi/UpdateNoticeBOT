import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()
from django.conf import settings

from webchecker.models import CafeMenuInfo, CafeMealTime, Guest
import telegram
from datetime import datetime, timedelta


bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)

def push_telegram():
    now = datetime.utcnow() + timedelta(hours=9) # KST
    if int(now.strftime('%H')) < 10:
        # Morning
        morning = CafeMealTime.objects.get(meal='morning')
        guests = Guest.objects.filter(meal_time=morning)
        today_meal = CafeMenuInfo.objects.get(date=datetime.now()).get_menu()
        for guest in guests:
            if len(today_meal[0]) > 3: # 휴무는 1
                bot.sendMessage(
                    chat_id=guest.telegram_id,
                    text='-- 아침 학식 --\n'
                         '{}'.format(today_meal[0])
                )
            else:
                bot.sendMessage(
                    chat_id=guest.telegram_id,
                    text='오늘은 아침 학식이 없습니다.'
                )
    elif int(now.strftime('%H')) < 14:
        # Lunch
        lunch = CafeMealTime.objects.get(meal='lunch')
        guests = Guest.objects.filter(meal_time=lunch)
        today_meal = CafeMenuInfo.objects.get(date=datetime.now()).get_menu()
        for guest in guests:
            if len(today_meal[1]) > 3:  # 휴무는 1
                bot.sendMessage(
                    chat_id=guest.telegram_id,
                    text='-- 점심 학식 --\n'
                         '{}'.format(today_meal[1])
                )
            else:
                bot.sendMessage(
                    chat_id=guest.telegram_id,
                    text='오늘은 점심 학식이 없습니다.'
                )
    else:
        # Dinner
        dinner = CafeMealTime.objects.get(meal='dinner')
        guests = Guest.objects.filter(meal_time=dinner)
        today_meal = CafeMenuInfo.objects.get(date=datetime.now()).get_menu()
        for guest in guests:
            if len(today_meal[2]) > 3:  # 휴무는 1
                bot.sendMessage(
                    chat_id=guest.telegram_id,
                    text='-- 저녁 학식 --\n'
                         '{}'.format(today_meal[2])
                )
            else:
                bot.sendMessage(
                    chat_id=guest.telegram_id,
                    text='오늘은 저녁 학식이 없습니다.'
                )


if __name__=='__main__':
    push_telegram()
