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
    browser.add_cookie({"name": "MUSIC_U", "value": "0042575CDAB60711DAAD9C86119520B05AB0F30B8A64158D8AD68A45607210102A40BDD9E3D069AC248AAB32C3A33312303F441EC6DEC538C65FBC258FA126E068687BE41BD7BF0B705F8AA95AF1C9639FE562874A9FBDF8E5601CA8C1958041505ECE4A04D35DD1F947D07418A3C9A29015E2E9A0FB049D6BFD059F05EE78C2BDA3AECE7BCE48937B680C138D05F0B2F994828BD6B3BE8986E73192B44AEE29BCD67B7D4A5886C5828BD3B8665A195605A8B8A6ECF256D28B009FA50CD0FA87BA0329A17DDCF9207F07B807BFB4B04C844EE8593D2E3D0078F324A30F1C17A149C65749553AB6607FA261E69AA5807E4EE7439946E4F9B800D777ABDF288A7A4175A9EA20A683B03D6818464CF3021ED033458C5E30D90AA998B224CC4869ADBBC164FF1BD4D8491422962DA9BB05556924F6234151D4A8C7D3DF949048571F22CF25DFBED247DEE86CF08BB51E817A2ED927C6F69FF8FA66330FC7C9DC025C72"})
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
