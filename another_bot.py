import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()

from django.conf import settings
from webchecker.models import *
from datetime import datetime, timedelta

from telegram.ext import Updater, CommandHandler

def start(bot, update):
    telegram_id = update.message['chat']['id']

    guest, is_created = Guest.objects.get_or_create(telegram_id=telegram_id)
    guest.save()

    options = Option.objects.all()
    option_list = ''
    for num, i in enumerate(options, start=1):
        option_list += (str(num) + '. [/' + i.name + ']: ' + i.description + '\n')

    update.message.reply_text(
        '안녕하세요,\n'
        'SNUE알림봇을 추가해주셔서 감사합니다.\n'
        'SNUE알림봇에는 여러 기능이 있습니다.\n'
        '원하는 기능을 터치해 서비스를 받아보세요.\n'
        '{}\n'.format(option_list))
    update.message.reply_text('자세한 안내가 필요하시면 [/help]를 터치해주세요!')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def help(bot, update):
    telegram_id = update.message['chat']['id']
    guest = Guest.objects.get(telegram_id=telegram_id)
    options = guest.using_options
    unused_options = guest.unused_options

    if options.count() > 0:
        option_list = ''
        for num, i in enumerate(options, start=1):
            option_list += (str(num) + '. [/' + i.name + '] : ' + i.description + '\n')
        update.message.reply_text(
            '현재 이용중이신 서비스는 {}가지 입니다.\n'
            '{}'
            ''.format(
                len(options),
                option_list,
            )
        )
    else:
        update.message.reply_text(
            '현재 이용중이신 서비스가 없습니다.\n'
            'SNUE봇의 여러 기능을 이용해보시는건 어떠신가요?'
        )

    if unused_options.count() > 0:
        unused_option_list = ''
        for num, i in enumerate(unused_options, start=1):
            unused_option_list += (str(num) + '. [/' + i.name + '] : ' + i.description + '\n')

        update.message.reply_text(
            '현재 이용가능한 서비스는 {}가지가 있습니다.\n'
            '사용을 원하시는 기능을 클릭해주세요.\n'
            '{}'
            ''.format(
                len(unused_options),
                unused_option_list,
            )
        )
    else:
        update.message.reply_text(
            'SNUE봇의 모든 기능을 이용하고 계시네요!\n'
            '감사합니다 :)'
        )

def notice(bot, update):
    telegram_id = update.message['chat']['id']

    guest = Guest.objects.get(telegram_id=telegram_id)
    notice = Option.objects.get(name='notice')
    if notice in guest.using_options:
        update.message.reply_text(
            '이미 SNUE 공지 알림에 등록되어 있습니다!\n'
            '새로운 공지사항이 오는 경우 즉시 알려드리고 있습니다 :)\n'
            '만약 알림을 받기를 원하지 않으신다면 [/notice_stop]을 터치해주세요.'
        )
        update.message.reply_text('자세한 안내가 필요하시면 [/help]를 터치해주세요.')

    else:
        guest.options.add(notice)
        guest.save()
        update.message.reply_text(
            'SNUE 공지 알림이 성공적으로 등록되었습니다!\n'
            '이시간 이후로 새로운 공지사항이 오는 경우 즉시 알려드리겠습니다 :)\n'
            '만약 알림을 받기를 원하지 않으신다면 [/notice_stop]을 터치해주세요.'
        )
        update.message.reply_text(
            '다른 기능을 추가로 이용하시려면 [/help]를 터치해주세요.'
        )

def notice_stop(bot, update):
    telegram_id = update.message['chat']['id']

    guest = Guest.objects.get(telegram_id=telegram_id)
    notice = Option.objects.get(name='notice')
    if notice in guest.using_options:
        guest.options.remove(notice)
        guest.save()
        update.message.reply_text(
            'SNUE 공지 알람을 끄셨습니다.\n'
            '만약 알림을 다시 받으시려면 [/notice]를 터치해주세요.'
        )
    else:
        update.message.reply_text(
            '아직 SNUE 공지 알람에 등록되어있지 않습니다.\n'
            '더 상세한 안내가 필요하시면 [/help]를 입력해주세요!'
        )

def cafeteria_morning(bot, update):
    telegram_id = update.message['chat']['id']
    guest = Guest.objects.get(telegram_id=telegram_id)
    morning = CafeMealTime.objects.get(meal='morning')
    today_meal = CafeMenuInfo.objects.get(date=datetime.now()).get_menu()[0] # 0, 1, 2
    if morning in guest.meal_time:
        update.message.reply_text(
            '이미 아침 학식알림을 받아보고 계시네요!\n'
            '만약 아침 학식 알림을 더이상 받지않으시려면,\n'
            '[/cafeteria_morning_stop]을 눌러주세요.'
        )
        update.message.reply_text(
            '오늘의 아침 학식은\n{}입니다.'.format(today_meal)
        )
    else:
        guest.meal_time.add(morning)
        update.message.reply_text(
            '아침 학식 알림이 등록되었습니다!\n'
            '매일 7:30AM에 오늘의 아침학식을 알려드릴게요.\n'
            '만약 아침 학식 알림을 더이상 받지않으시려면,\n'
            '[/cafeteria_morning_stop]을 눌러주세요.'
        )
        update.message.reply_text(
            '오늘의 아침 학식은\n{}입니다.'.format(today_meal)
        )

def cafeteria_morning_stop(bot, update):
    telegram_id = update.message['chat']['id']
    guest = Guest.objects.get(telegram_id=telegram_id)
    morning = CafeMealTime.objects.get(meal='morning')
    if morning in guest.meal_time:
        guest.meal_time.remove(morning)
        update.message.reply_text(
            '아침 학식알림을 끄셨습니다.\n'
            '만약 아침 학식 알림을 다시 받으시려면,\n'
            '[/cafeteria_morning]을 눌러주세요.'
        )
    else:
        guest.meal_time.add(morning)
        update.message.reply_text(
            '아직 아침 학식알림을 켜지 않으셨습니다!\n'
            '매일 7:30AM에 아침학식 알림을 받으시려면,\n'
            '[/cafeteria_morning]을 눌러주세요.'
        )

def cafeteria_lunch(bot, update):
    telegram_id = update.message['chat']['id']
    guest = Guest.objects.get(telegram_id=telegram_id)
    lunch = CafeMealTime.objects.get(meal='lunch')
    today_meal = CafeMenuInfo.objects.get(date=datetime.now()).get_menu()[1] # 0, 1, 2
    if lunch in guest.meal_time:
        update.message.reply_text(
            '이미 점심 학식알림을 받아보고 계시네요!\n'
            '만약 점심 학식 알림을 더이상 받지않으시려면,\n'
            '[/cafeteria_lunch_stop]을 눌러주세요.'
        )
        update.message.reply_text(
            '오늘의 점심 학식은\n{}입니다.'.format(today_meal)
        )
    else:
        guest.meal_time.add(lunch)
        update.message.reply_text(
            '점심 학식 알림이 등록되었습니다!\n'
            '매일 12시에 오늘의 아침학식을 알려드릴게요.\n'
            '만약 점심 학식 알림을 더이상 받지않으시려면,\n'
            '[/cafeteria_lunch_stop]을 눌러주세요.'
        )
        update.message.reply_text(
            '오늘의 점심 학식은\n{}입니다.'.format(today_meal)
        )

def cafeteria_lunch_stop(bot, update):
    telegram_id = update.message['chat']['id']
    guest = Guest.objects.get(telegram_id=telegram_id)
    lunch = CafeMealTime.objects.get(meal='lunch')
    if lunch in guest.meal_time:
        guest.meal_time.remove(lunch)
        update.message.reply_text(
            '점심 학식알림을 끄셨습니다.\n'
            '만약 점심 학식 알림을 다시 받으시려면,\n'
            '[/cafeteria_lunch]을 눌러주세요.'
        )
    else:
        guest.meal_time.add(lunch)
        update.message.reply_text(
            '아직 점심 학식알림을 켜지 않으셨습니다!\n'
            '매일 12시에 점심 학식 알림을 받으시려면,\n'
            '[/cafeteria_lunch]을 눌러주세요.'
        )

def cafeteria_dinner(bot, update):
    telegram_id = update.message['chat']['id']
    guest = Guest.objects.get(telegram_id=telegram_id)
    dinner = CafeMealTime.objects.get(meal='dinner')
    today_meal = CafeMenuInfo.objects.get(date=datetime.now()).get_menu()[2] # 0, 1, 2
    if dinner in guest.meal_time:
        update.message.reply_text(
            '이미 저녁 학식알림을 받아보고 계시네요!\n'
            '만약 저녁 학식 알림을 더이상 받지않으시려면,\n'
            '[/cafeteria_dinner_stop]을 눌러주세요.'
        )
        update.message.reply_text(
            '오늘의 저녁 학식은\n{}입니다.'.format(today_meal)
        )
    else:
        guest.meal_time.add(dinner)
        update.message.reply_text(
            '저녁 학식 알림이 등록되었습니다!\n'
            '매일 저녁 5시에 오늘의 아침학식을 알려드릴게요.\n'
            '만약 저녁 학식 알림을 더이상 받지않으시려면,\n'
            '[/cafeteria_dinner_stop]을 눌러주세요.'
        )
        update.message.reply_text(
            '오늘의 저녁 학식은\n{}입니다.'.format(today_meal)
        )

def cafeteria_dinner_stop(bot, update):
    telegram_id = update.message['chat']['id']
    guest = Guest.objects.get(telegram_id=telegram_id)
    dinner = CafeMealTime.objects.get(meal='dinner')
    if dinner in guest.meal_time:
        guest.meal_time.remove(dinner)
        update.message.reply_text(
            '저녁 학식알림을 끄셨습니다.\n'
            '만약 저녁 학식 알림을 다시 받으시려면,\n'
            '[/cafeteria_dinner]을 눌러주세요.'
        )
    else:
        guest.meal_time.add(dinner)
        update.message.reply_text(
            '아직 저녁 학식알림을 켜지 않으셨습니다!\n'
            '매일 저녁 5시에 저녁 학식 알림을 받으시려면,\n'
            '[/cafeteria_dinner]을 눌러주세요.'
        )



updater = Updater(settings.TELEGRAM_TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('notice', notice))
updater.dispatcher.add_handler(CommandHandler('notice_stop', notice_stop))
updater.dispatcher.add_handler(CommandHandler('cafeteria_morning', cafeteria_morning))
updater.dispatcher.add_handler(CommandHandler('cafeteria_morning_stop', cafeteria_morning_stop))
updater.dispatcher.add_handler(CommandHandler('cafeteria_lunch', cafeteria_lunch))
updater.dispatcher.add_handler(CommandHandler('cafeteria_lunch_stop', cafeteria_lunch_stop))
updater.dispatcher.add_handler(CommandHandler('cafeteria_dinner', cafeteria_dinner))
updater.dispatcher.add_handler(CommandHandler('cafeteria_dinner_stop', cafeteria_dinner_stop))

updater.start_polling()
updater.idle()