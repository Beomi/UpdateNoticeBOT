from django import forms

from .models import CustomNotice


class CustomNoticeForm(forms.ModelForm):
    class Meta:
        model = CustomNotice
        fields = ['title', 'content', ]
