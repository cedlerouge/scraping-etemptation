#!/usr/bin/env python 

# ref :  https://www.scrapingbee.com/blog/selenium-python/


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time
import json
import os
import shutil

_config_filename = './settings.json'

def get_driver(driver="chrome"):
    # the chrome_bin must be the real binary, it mustn't be a link to the binary
    chrome_bin = "/opt/google/chrome/google-chrome"
    #chromedriver_bin = '/home/XXX/.wdm/drivers/chromedriver/linux64/136.0.7103.113/chromedriver-linux64/chromedriver'

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--verbose')
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument(r'--disable-blink-features=AutomationControlled')
    options.binary_location = chrome_bin


    #service = webdriver.ChromeService(executable_path=chromedriver_bin)
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

if __name__ == '__main__':

    # Get configuration from json file
    config = json.loads(open(_config_filename).read())

    if "browser" in config.keys() :
        browser = get_driver(driver=config["browser"])
    else:
        print("ERROR: You have to define a browser in the settings.json file")
        os.exit(1)


    print("test1")
    if "website_url" in config.keys():
        browser.get(config["website_url"])
    else:
        print("ERROR: You have to define website_url in settings.json file")
        os.exit(1)

    print("Etemptation Authentication")
    if "username" in config.keys() and "password" in config.keys():
        username = browser.find_element(By.ID, "USERID").send_keys(config["username"])
        password = browser.find_element(By.ID, "XXX_PASSWORD").send_keys(config["password"])
        submit = browser.find_element(By.ID, "connect").click()
    else:
        print("ERROR: You have to define username and password in settings.json file")
        os.exit(1)

    try:
        logout_button = browser.find_element(By.ID, "disconnect")
        print("Successfully logged in to Etemptation")
    except:
        print("Incorrect login/password")

    print("Make a declaration for lunch ticket")
    menu = browser.find_element(By.LINK_TEXT, 'Self service').click()
    time.sleep(1)
    ticket_repas = browser.find_element(By.PARTIAL_LINK_TEXT, "Demande de Titre Repas").click()
    time.sleep(1)
    bouton_demande = browser.find_element(By.XPATH, "//input[@value='Nouvelle demande']").click()
    time.sleep(1)

    form_motif = browser.find_element(By.ID, "for/MOTIF").send_keys("ZTCKREST")
    
    form_nombre = browser.find_element(By.ID, "VALDEB_N_label").click()
    form_valeur = browser.find_element(By.ID, "for/MOTIDUR").send_keys("1.00")
    time.sleep(1)


    bouton_valider = browser.find_element(By.ID, "_MODAL_BTNA").click()
    time.sleep(1)

    validation_message = "Votre déclaration a été prise en compte"
    error_message = "Solde insuffisant pour ce motif"
    error = False

    validation = browser.find_element(By.ID, "modale_content")
    if validation_message in validation.text:
        print("Successfully declared")
    else:
        if error_message in validation.text:
            print("Couldn't declare: ", error_message)
            error = True

    try:
        validation = browser.find_element(By.ID, "modale_content")
        if validation_message in validation.text:
            print("Successfully declared")
        else:
            if error_message in validation.text:
                print("Couldn't declare: ", error_message)
                error = True
    except:
        print("Couldn't ask for lunch ticket")

    print("Closing message pop up")
    logout_button = browser.find_element(By.ID, "_MODALMSG_BTNA").click()

    if error:
        print('Closing declaration pop up: Canceling')
        logout_button = browser.find_element(By.ID, "_MODAL_BTNB").click()


    print("Logout")
    logout_button = browser.find_element(By.ID, "disconnect").click()
    print("done")

    browser.quit()
