from selenium import webdriver
from datetime import datetime
import pytz

def _get_contents(usr_id, usr_pw):
    # Base Setup
    driver = webdriver.PhantomJS(executable_path='phantomjs', service_args=['--ignore-ssl-errors=true'])
    driver.implicitly_wait(1)
    base_url = 'https://portal.snue.ac.kr/'

    # Login
    driver.get(base_url + "enview/user/login.face")
    driver.find_element_by_name("userId").clear()
    driver.find_element_by_name("userId").send_keys(usr_id)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(usr_pw)
    driver.find_element_by_xpath('//*[@id="btn_login"]/input').click()

    # Get HTML
    driver.get(base_url + 'enview/snue/SNUE06.face?cutLength=200&pageSize=100')
    titles = driver.find_elements_by_xpath('/html/body/div/ul/li/a')
    dates = driver.find_elements_by_xpath('/html/body/div/ul/li/span')

    result = []

    if len(titles)==len(dates):
        for i in range(len(titles)):
            title = titles[i].text
            url = titles[i].get_attribute('href')
            date = dates[i].text
            py_date = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
            tp = dict(title=title, url=url, py_date=py_date, date=date)
            result.append(tp)

    return result
