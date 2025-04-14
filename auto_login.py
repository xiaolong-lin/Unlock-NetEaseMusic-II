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
    browser.add_cookie({"name": "MUSIC_U", "value": "00597039B4672E7047F9C1614D6407F4FC68D7D0A0DBE1FCD4781B97C48809F166ED0ACEB687A2536CEAF928E2E5A022061E61B075A8716FB750FEAF152964567EF2CCF00A7C1511BA497DC322F77A92B12F0A028D1B2ABA986931ED166B4995AE227F651450C7D001E51BA1F62242CEAEFB6121FC5B7683427CED0CB359001692EDA479AA0DD35C76C1167018867F4AD26F0D13EEE8FE4A2F9E7BF1920F690BC952852C8EC2F6A132A89A879FD71D13568577B031151E9172A952D2E4942B66103B2EA727D0F659D5531FCB992873D584255FCBC7C8E04386067C9AC7D33AF6519AB197F44A63179332C41540B5E713034947C9846F6CE3258369D4770027703B3CBFAC38489EB97845E8E6BE7FDFEDD5D27B0A236F301471D5DCA711759B5091C7E15B316253205A259EB01DDBC16FFD111128BEF049181FCF19121639A458984733DA5DFFAD2C0208C722635CA9878D5FEE5B0DE3E749936EC2EDFA84CAF73A"})
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
