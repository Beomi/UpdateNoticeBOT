from django.shortcuts import render

from .forms import CustomNoticeForm


def custom_notice(request):
    if request.method == 'POST':
        form = CustomNoticeForm(request.POST)
    else:
        form = CustomNoticeForm()

    return render(request, 'webchecker/custom_notice.html', {
        'form': form,
    })