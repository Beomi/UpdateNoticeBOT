from django.db import models

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
