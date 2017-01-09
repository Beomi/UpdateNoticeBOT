import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UpdateNoticeBOT.settings")
import django
django.setup()

from webchecker.cafeteria_parser import _get_menus

from webchecker.models import CafeMenuInfo

# execute every week, monday morning at 7:30am

def update_cafe_menu_info():
    new_menus = _get_menus()
    for menu_i in new_menus:
        cmi = CafeMenuInfo(
            date=menu_i[0]
        )
        cmi.set_menu(menu_i[1])
        cmi.save()


if __name__=='__main__':
    update_cafe_menu_info()