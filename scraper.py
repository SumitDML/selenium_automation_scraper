from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

def highlight(element):
    driver.execute_script("arguments[0].style.border='3px solid red'", element)

chrome_options = Options()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

titles = []

try:
    driver.get("https://app.acvauctions.com/login")
    time.sleep(2)

    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'login_email'))
    )
    highlight(email_field)
    password_field = driver.find_element(By.ID, 'login_password')
    highlight(password_field)

    email_field.send_keys("arbitrinc@gmail.com")
    password_field.send_keys("Michael123*")
    time.sleep(2)

    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    highlight(login_button)
    driver.save_screenshot('before_login_click.png')
    login_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'acv-infinite-scroller-item'))
    )
    driver.save_screenshot('after_login.png')

    items = driver.find_elements(By.CLASS_NAME, 'acv-infinite-scroller-item')

    for item in items:
        highlight(item)
        time.sleep(1)

        try:
            title_element = item.find_element(By.CLASS_NAME, 'title')
            highlight(title_element)
            title_text = title_element.text
            print(title_text)
            titles.append(title_text) 
        except:
            print("No title found in this item")

finally:
    df = pd.DataFrame(titles, columns=["TITLE"])
    df.to_excel('scraped_titles.xlsx', index=False)

    driver.quit()
