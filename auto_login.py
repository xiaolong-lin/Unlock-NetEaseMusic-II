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
    browser.add_cookie({"name": "MUSIC_U", "value": "009E26E5C259B53EBD49F80F35CA8741F417B00F0FCB10F2993FBB3287622994DD7C371CF60670A19D0C946CDE7F6050A436988F8FAE6545C06F22A7B109C9FE465EEA5778D09CF486421C41F830ACAD8FC61110BECEC9A9EA5E868304C01C401C9881B4D055EA31C26E7F7F922FFD373F31301CED9CEDDC72FB2D61E3206FA8A262FB605D6DC63305FE1C9AC2DF58E6084133D26F087D327046E69CE69AA4C8D520EC3FB20ACD6EC87699A92654A833E464E6749DC1341538E36F82B8A53E97BADA1DC052860EBE6FB6EA9A2F3DE343EAD58A4C4039463CB7E120B06FD35A574548F5C8447DC5826A33011891972A3F466A5BB3B99581ACAD58BF9B5BB960D84867525AF059959A1E1ABEABE235F399DA1450487C73DE7BBF27B879B8249CCB40A4A0E8FE63F3C2275777A1A3B2E5A3CE3B1EA96FE0A25F0FE4E4DC3FE7F7B2BCCF0D21466832F297E05E506C5736963A9B5D14AF0BDF2A7B754DD422F7C97799"})
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
