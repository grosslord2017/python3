'''Завдання: за допомогою браузера (Selenium) відкрити форму за наступним посиланням:
https://docs.google.com/forms/d/e/1FAIpQLScLhHgD5pMnwxl8JyRfXXsJekF8_pDG36XtSEwaGsFdU2egyw/viewform?usp=sf_link
заповнити і відправити її.
Зберегти два скріншоти: заповненої форми і повідомлення про відправлення форми.
В репозиторії скріншоти зберегти.'''

from time import sleep
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = wd.ChromeOptions()
options.add_argument("--no-sandbox")
url_form = 'https://docs.google.com/forms/d/e/1FAIpQLScLhHgD5pMnwxl8JyRfXXsJekF8_pDG36XtSEwaGsFdU2egyw/viewform?usp=sf_link'
name = 'Vitalii'

driver = wd.Chrome(executable_path='./chromedriver', options=options)
driver.get(url_form)
wait = WebDriverWait(driver, 10)

block = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="listitem"]')))
text = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]')))
# text = block.find_element(By.CSS_SELECTOR, 'input[type="text"]')
# sleep(5)
text.send_keys(name)
driver.save_screenshot('first_screen.png')
button = driver.find_element(By.CSS_SELECTOR, '.freebirdFormviewerViewFormContent .freebirdFormviewerViewNavigationLeftButtons span')
button.click()
new_page = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.freebirdFormviewerViewResponseConfirmContentContainer')))
driver.save_screenshot('second_screen.png')


driver.close()