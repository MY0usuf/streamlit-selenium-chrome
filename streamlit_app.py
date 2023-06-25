import streamlit as st
import os
import time

"""
## Web scraping on Streamlit Cloud with Selenium

[![Source](https://img.shields.io/badge/View-Source-<COLOR>.svg)](https://github.com/snehankekre/streamlit-selenium-chrome/)

This is a minimal, reproducible example of how to scrape the web with Selenium and Chrome on Streamlit's Community Cloud.

Fork this repo, and edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:
"""

def scroll_down(driver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight/4);')

base_url = 'https://dubailand.gov.ae/en/open-data/real-estate-data/#/'
chrome_file = '\\chromedriver.exe'
download_dir = os.getcwd() + '\\download_csv'
transaction_dir = os.getcwd() + '\\transaction_csv'

with st.echo():
    import datetime
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC


    @st.experimental_singleton
    def get_driver():
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    date = datetime(2023,6,23)

    options = Options()
    options.add_experimental_option('prefs',  {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
    "pdfjs.disabled": True
    }
    )
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')

    driver = get_driver()

    # Getting Todays Date and Month to use while filling out the form
    day = date.strftime('%d')
    month_int = int(date.strftime('%m'))
    month = str(month_int - 1)
    year = date.strftime('%Y')
    #month = str(month - 1)


    driver.get(base_url)
    driver.implicitly_wait(0.5) 

    action = ActionChains(driver)

    # Switching the navbar to Transactions tab if necessary
    transaction_element = driver.find_element(By.LINK_TEXT, 'Transactions')
    driver.implicitly_wait(1)
    transaction_element.click()
    time.sleep(4)

    # Finding the from date form element to enter the date
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "transaction_pFromDate")))
    from_date_picker = driver.find_element(By.ID, 'transaction_pFromDate')
    from_date_picker.click()
    from_date_picker.clear()
    from_date_picker.send_keys(f'{day}/{month_int}/{year}')
    driver.implicitly_wait(1)

    # Selecting the current month in the datepicker UI
    select_month_from_date = Select(driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]'))
    select_month_from_date.select_by_value(month)

    # Finding the to date form element to enter the date
    to_date_picker = driver.find_element(By.ID, 'transaction_pToDate')
    to_date_picker.click()
    to_date_picker.clear()
    to_date_picker.send_keys(f'{day}/{month_int}/{year}')
    select_month_to_date = Select(driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]'))
    select_month_to_date.select_by_value(month)
    
    scroll_down(driver)
    search_csv = driver.find_element(By.XPATH, '//*[@id="trxFilter"]/div/div[10]/div/button[1]')
    time.sleep(2)
    search_csv.click()
    time.sleep(10)
    scroll_down(driver)
    time.sleep(2)
    download_csv = driver.find_element(By.XPATH, '//*[@id="transaction"]/div/div/div[1]/div/div/button')
    time.sleep(1)
    download_csv.click()
    time.sleep(4)
    driver.quit()
    for file in os.listdir('download_csv'):
        if file.endswith('csv'):
            os.rename(os.path.join(download_dir,file),os.path.join(transaction_dir,f'data_{date}.csv'))
    st.code(driver.page_source)
