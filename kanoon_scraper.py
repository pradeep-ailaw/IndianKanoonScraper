from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import os
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


CHROME_DRIVER_PATH = "XX/XX/XX/chromedriver-win64/chromedriver-win64/chromedriver.exe" #link to chromedriver exe here
URL = 'https://indiankanoon.org/browse/greentribunal/{}/'
BASE_URL = "https://indiankanoon.org" 
DOWNLOAD_DIR = f"{os.getcwd()}\\green-tribunal-2022\\" # set download file location

# Enter username and password here if downloading court copies
USERNAME = "xyz@gmail.com"
PASSWORD = "abc123"


driver = webdriver.Chrome(CHROME_DRIVER_PATH)


def get_url(year):
    url = URL.format(year)
    return url


def get_inner_link(year):    
    page = [] 
    url = get_url(year)
    driver.get(url.format(page)) 
    
    soup = BeautifulSoup(driver.page_source, 'html.parser') 
    result = soup.find('div', {'class':'info_indian_kanoon'}) 
    link = [BASE_URL + td.a['href'] for td in result.table.find_all('td')]
    
    return link

def sorting(year, month):
    links = get_inner_link(year)
    inner_link = links[month]
    
    url1 = inner_link
    driver.get(url1)
    
    element_dropdown = driver.find_element_by_id('sortbySelect')
    select = Select(element_dropdown)
    select.select_by_visible_text('Most Recent')
    link1 = url1 + '+sortby%3Amostrecent'
    
    return link1

def most_recent_record(year, month, num_records):
    link2 = sorting(year, month)
    page = []
    driver.get(link2.format(page))
    base_url = "https://indiankanoon.org"
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    result = soup.findAll('div', class_ = 'result')
    link2 = [base_url + div.a['href'] for div in result]
    return link2[:num_records]

def main_url(year, month):
    link3 = most_recent_record(year, month, num_records=5)
    return link3

def login(driver, username, password):
    login_url = "https://indiankanoon.org/members/login/?nextpage=/"
    driver.get(login_url)
    driver.find_element(By.NAME, "email").send_keys(username)
    driver.find_element(By.NAME, "passwd").send_keys(password)
    driver.find_element(By.XPATH, "//input[@class='submit_button' and @type='submit']").click()
    

chromedriver_autoinstaller.install()
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

preferences = {"download.default_directory": DOWNLOAD_DIR,
                # "download.prompt_for_download": False,
                # "directory_upgrade": True,
                # "safebrowsing.enabled": True
                }
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", preferences)
driver = webdriver.Chrome(chrome_options=chromeOptions)


def download(year, court_copy=False): 
    if court_copy:
        login(driver, USERNAME, PASSWORD)
        button_text = 'Download Court Copy'
    else:
        button_text = 'Get this document in PDF'
        
    for month in range(1, 13):
        urls = main_url(year, month) 

        for url in urls:
            driver.get(url)
            try:
                download_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(),'{button_text}')]"))
                )
                download_button.click()
                time.sleep(2)  # prevents robot check
            except TimeoutException:
                print(f"Download button not found for URL: {url}")
            except Exception as e:
                print(f"Error: {e}")


download(2022, court_copy=False)

