import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()

from webchecker.models import ParsedData

print(ParsedData.objects.all())