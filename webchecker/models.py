from django.db import models
from django.db.models import Q

import json


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ParsedData(TimeStampModel):
    title = models.CharField(max_length=200)
    url = models.URLField()
    py_date = models.DateTimeField()
    date = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Guest(TimeStampModel):
    telegram_id = models.CharField(max_length=200)
    options = models.ManyToManyField('Option', blank=True)
    meal_time = models.ManyToManyField('CafeMealTime', blank=True)

    def __str__(self):
        return self.telegram_id

    @property
    def using_options(self):
        return self.options.all()

    @property
    def unused_options(self):
        return Option.objects.exclude(pk__in=self.using_options)


class Option(TimeStampModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    telegram_command = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def list_of_using_guests(self):
        return self.objects.prefetch_related('guest_set__using_options').all()


class CafeMenuInfo(TimeStampModel):
    date = models.DateField()
    menu = models.TextField()

    def set_menu(self, x):
        self.menu = json.dumps(x)

    def get_menu(self):
        return json.loads(self.menu)

    def __str__(self):
        return str(self.date)


class CafeMealTime(TimeStampModel):
    MEAL_TIMES = (
        ('morning', 'morning'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
    )

    meal = models.CharField(max_length=20, choices=MEAL_TIMES, unique=True)

    def __str__(self):
        return self.meal


class CustomNotice(TimeStampModel):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

