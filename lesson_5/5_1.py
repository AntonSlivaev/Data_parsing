from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['mails']

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru/')

username = driver.find_element_by_id('mailbox:login')
username.send_keys('study.ai_172@mail.ru')
username.send_keys(Keys.ENTER)

password = driver.find_element_by_id('mailbox:password')
password.send_keys('NextPassword172')
time.sleep(2)
password.send_keys(Keys.RETURN)

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'js-letter-list-item')))

button = driver.find_element_by_class_name('settings')
button.click()
time.sleep(1)
try:
    group = driver.find_element_by_class_name('checkbox__box_checked')
    group.click()
except:
    print('группировка ')
time.sleep(1)

links, last_mail = set(), 0

while True:
    mails = driver.find_elements_by_class_name('js-letter-list-item')

    if mails[-1] == last_mail:
        break
    else:
        last_mail = mails[-1]

    for mail in mails:
        link = mail.get_attribute('href')
        links.add(link)
    actions = ActionChains(driver)
    actions.move_to_element(last_mail)
    actions.perform()

links = list(links)
for link in links:
    driver.get(link)
    subject = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject')))
    author = driver.find_element_by_class_name('letter-contact')
    date = driver.find_element_by_class_name('letter__date')
    text = driver.find_element_by_class_name('letter__body')
    db.mail_ru.insert_one({'author': author.text, 'date': date.text, 'subject': subject.text, 'text': text.text})

driver.close()