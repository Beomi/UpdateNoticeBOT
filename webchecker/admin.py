from django.contrib import admin
from .models import ParsedData, Guest, Option, CafeMenuInfo, CafeMealTime

admin.site.register(ParsedData)
admin.site.register(Guest)
admin.site.register(Option)
admin.site.register(CafeMenuInfo)
admin.site.register(CafeMealTime)