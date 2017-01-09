import requests
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime

def _get_menus():
    html = requests.get('http://portal.snue.ac.kr/enview/2015/food.jsp').text
    soup = bs(html, 'html.parser')
    daily = soup.select(
        'tr'
    )

    re_date = re.compile('(\d{2}[/]\d{2})')

    menus = []

    for i in daily:
        try:
            info = i.text.split('\n')
            date = re.search(re_date, info[1]).group()

            py_date = datetime.strptime(date, '%m/%d').replace(year=datetime.today().year)
            morning_meal = info[2].replace(' ', '\n')
            lunch_meal = info[3].replace(' ', '\n')
            dinner_meal = info[4].replace(' ', '\n')
            menus.append([py_date, [morning_meal, lunch_meal, dinner_meal]])
        except AttributeError:
            pass # to ignore first tr

    return menus

if __name__=='__main__':
    print(_get_menus())


