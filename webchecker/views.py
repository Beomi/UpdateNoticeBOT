from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

import telegram

from .forms import CustomNoticeForm

from .models import Guest


def custom_notice(request):
    if request.method == 'POST':
        form = CustomNoticeForm(request.POST)
        if form.is_valid():
            bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
            #guests = Guest.objects.filter(options='student_union_notice')
            guests = Guest.objects.all()
            for guest in guests:
                bot.sendMessage(
                    chat_id=guest.telegram_id,
                    text=form.cleaned_data.get('title') + '\n\n' + form.cleaned_data.get('content')
                )
            form.save()
            return JsonResponse({
                'message': '성공적으로 메시지가 전송되었습니다.'
            })
        else:
            return JsonResponse({
                'message': '제목과 내용을 정확히 입력해주세요.'
            })
    else:
        form = CustomNoticeForm()

    return render(request, 'webchecker/custom_notice.html', {
        'form': form,
    })
