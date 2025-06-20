
import os
import time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Загрузка переменных из .env
load_dotenv()
USERNAME = os.getenv("TWITTER_USERNAME")
PASSWORD = os.getenv("TWITTER_PASSWORD")

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

def login():
    driver.get("https://twitter.com/login")
    wait = WebDriverWait(driver, 20)
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    username_input.send_keys(USERNAME)
    username_input.send_keys(Keys.RETURN)
    time.sleep(2)

    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

def get_pinned_tweet_link():
    driver.get(f"https://twitter.com/{USERNAME}")
    wait = WebDriverWait(driver, 10)
    pinned = wait.until(EC.presence_of_element_located((By.XPATH, "//article[contains(., 'Pinned Tweet')]")))
    tweet = pinned.find_element(By.XPATH, ".//a[@href and contains(@href, '/status/')]")
    link = tweet.get_attribute("href")
    return link

def send_message_to_groups(pinned_link):
    driver.get("https://twitter.com/messages")
    time.sleep(5)

    wait = WebDriverWait(driver, 10)
    chats = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/messages/')]")))

    chat_links = list(set([chat.get_attribute("href") for chat in chats if "/messages/" in chat.get_attribute("href")]))
    print(f"Found {len(chat_links)} groups")

    for link in chat_links:
        driver.get(link)
        time.sleep(random.randint(5, 10))
        try:
            msg_area = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='dmComposerTextInput']"))
            )
            msg_area.click()
            msg_area.send_keys(f"SFS please 🔁❤️\n{pinned_link}")
            msg_area.send_keys(Keys.RETURN)
            print(f"Sent to: {link}")
        except:
            print(f"Failed to send message to: {link}")
        time.sleep(random.randint(15, 40))

if __name__ == "__main__":
    login()
    pinned = get_pinned_tweet_link()
    send_message_to_groups(pinned)
    driver.quit()
