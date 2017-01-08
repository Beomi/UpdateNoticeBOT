from django.db import models
from django.db.models import Q


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

    def __str__(self):
        return self.telegram_id

    @property
    def using_options(self):
        return Option.objects.filter(guest__options__guest=self)

    @property
    def unused_options(self):
        return Option.objects.exclude(guest__options__guest=self)


class Option(TimeStampModel):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

    def list_of_using_guests(self):
        return self.objects.prefetch_related('guest_set__using_options').all()