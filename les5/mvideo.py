from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


client = MongoClient('127.0.0.1', 27017)
db = client['selenium']
db_hits = db.hits

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'gallery-layout_product-set')))

#  Создаем множество, в которое будем записывать информацию о товаре (в виде словарей). Переменная set_length -
# длина множества - создается для контроля того, что информация о товарах не начала повторяться.
hits_set = set()
set_length = 0
while True:
    hits = driver.find_elements_by_xpath("//div[contains(text(), 'Хиты продаж')]/ancestor::div[contains(@class, "
                                         "'product-set')]//a[contains(@class, 'fl-product-tile-picture')]")
    for hit in hits:
        hits_set.add(hit.get_attribute('data-product-info'))
    new_set_length = len(hits_set)
    if new_set_length == set_length:
        break
    set_length = new_set_length
    arrow = driver.find_element_by_xpath("//div[contains(text(), 'Хиты продаж')]/ancestor::div[contains(@class, "
                                         "'product-set')]//a[contains(@class, 'i-icon-fl-arrow-right')]")
    arrow.click()
    time.sleep(5)

#  Записываем множество в базу, при этом с помощью функции eval превращаем элементы множества в нормального вида словарь
for hit in hits_set:
    db_hits.insert_one(eval(hit))


driver.close()
