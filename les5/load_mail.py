from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

client = MongoClient('127.0.0.1', 27017)
db = client['selenium']
db_mails = db.mails

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru/')

elem = driver.find_element_by_class_name('email-input')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_class_name('svelte-no02r')
elem.click()

elem = driver.find_element_by_class_name('password-input')
elem.send_keys('NextPassword172')

elem = driver.find_element_by_class_name('second-button')
elem.click()

#  Собираем ссылки на письма
links = set()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'llc')))


mails = driver.find_elements_by_class_name('llc')
for mail in mails:
    links.add(mail.get_attribute('href'))

last_mail_href = ''
while True:
    time.sleep(2)
    mails = driver.find_elements_by_class_name('llc')
    href = mails[-1].get_attribute('href')
    if href == last_mail_href:
        break
    else:
        for mail in mails:
            links.add(mail.get_attribute('href'))
    last_mail_href = href
    actions = ActionChains(driver)
    actions.move_to_element(mails[-1])
    actions.perform()

#  Собираем информацию по каждому из писем множества links
for link in links:
    driver.get(link)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__author')))
    except Exception:
        print('Не удалось загрузить письмо: ', link)
        continue
    sender_elem = driver.find_element_by_class_name('letter-contact')
    date_elem = driver.find_element_by_class_name('letter__date')
    title_elem = driver.find_element_by_class_name('thread__subject')
    content_elem = driver.find_element_by_class_name('letter__body')
    mail = {'sender': sender_elem.text, 'date': date_elem.text, 'title': title_elem.text, 'content': content_elem.text}
    db_mails.insert_one(mail)


driver.close()
