# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0081C87F0EB644C27CEBCC54ADCC324F3146376AB1FDDF819786A1FE06DF4943559BAA0629F7AAD5063BE1DCD23F3BEF03010B30EFEEEB6F17A2CAD0D54726A83E60D5732FC6D3388F44B2FD5CC203C80AEAEE69945854FCE910519785A6F762406D938B44ED0140A3E46D2C4358BD948C1EF58C5279CB8054554395E7C9BA23539B2C1984B7A816C2A96B7DB1D54E7A50DDE9D9120C4488DF2A582F1CB998A3CC0E1A77AD64E902B17D20F9E16072D0121114B14C21C473C1D56E3608AF542670EB7D3256F09067A5139CE0F2C28B9626FFB53762370AD91DFD4864F0299E6E5CC53B1F7EED6D52E8B3FA203D3329861F077C9F1ACEBC542E463405EB360D0B7E256405E87A739B9696CD8A7883A82C2B92CFE05108C88BB53D1A14358F4D375741A853816263795F568180FFF190357CD3303600611485BD7B3FD122BD77627B1E4DBE5055DD2657564CB8D4C38B55C0FEB8872D9A975D64DBFFE5DD1B5EABE8"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
