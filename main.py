from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import time

GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLScKOhs9AaKtXe1sS95YHi0SWzX63QaereoNgAshYXX8pdRYbw/viewform?usp=sf_link'
URL = 'https://appbrewery.github.io/Zillow-Clone/'
DATA = {}

#scraping data from the given URL

def create_data():
    global DATA
    respons = requests.get(url=URL)

    zillow_clone = respons.text

    soup = BeautifulSoup(zillow_clone, 'html.parser')

    links_elements = soup.find_all('a', {'data-test': 'property-card-link'})
    links_doubled = [elem['href'] for elem in links_elements]
    links = [elem for ind, elem in enumerate(links_doubled) if elem not in links_doubled[:ind]]

    address_elements = soup.find_all('address', {'data-test': 'property-card-addr'})
    addresses = [elem.get_text(strip=True) for elem in address_elements]

    price_elements = soup.find_all('span', {'data-test': 'property-card-price'})
    prices = [elem.get_text(strip=True) for elem in price_elements]

    DATA = {}

    for _ in range(0, len(links)):
        DATA[f'Option {_}'] = {}
        DATA[f'Option {_}']['link'] = f'{links[_]}'
        DATA[f'Option {_}']['address'] = f'{addresses[_]}'
        DATA[f'Option {_}']['price'] = f'{prices[_]}'


create_data()
print(DATA['Option 0']['link'])


#fills google forms automatically with the given data
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)
driver.get(GOOGLE_FORM_URL)
time.sleep(1)

for _ in DATA:
    input_fields = driver.find_elements(By.CLASS_NAME, 'whsOnd')

    input_fields[0].send_keys(DATA[_]['address'])
    input_fields[1].send_keys(DATA[_]['price'])
    input_fields[2].send_keys(DATA[_]['link'])

    send_button = driver.find_element(By.CLASS_NAME, 'l4V7wb')
    send_button.click()
    time.sleep(1)


    another_answer_page = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_answer_page.click()
    time.sleep(2)

driver.quit()
