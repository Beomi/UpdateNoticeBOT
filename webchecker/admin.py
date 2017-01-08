from django.contrib import admin
from .models import ParsedData, Guest, Option

admin.site.register(ParsedData)
admin.site.register(Guest)
admin.site.register(Option)