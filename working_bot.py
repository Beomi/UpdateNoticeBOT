import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()

from webchecker.models import ParsedData

f = open('some.txt','w+')
f.write(str(ParsedData.objects.all()))
f.close()

print('finish')
