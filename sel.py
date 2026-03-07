import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]


def get(cols, i):
    return cols[i].text.strip() if len(cols) > i else ""


options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 30)

timetable = []

try:

    # open login page
    driver.get("https://www.go4schools.com/sso/account/login?site=Student")

    username = wait.until(
        EC.presence_of_element_located((By.ID, "usernameInput"))
    )
    username.send_keys(USERNAME)

    password = driver.find_element(By.ID, "passwordInput")
    password.send_keys(PASSWORD)
    password.send_keys(Keys.RETURN)

    # try to wait for timetable rows
    try:
        rows = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.ghost-content"))
        )
    except TimeoutException:
        rows = []

    # scrape timetable if rows exist
    for row in rows:

        cols = row.find_elements(By.XPATH, "./th|./td")

        if len(cols) < 6:
            continue

        timetable.append({
            "start": get(cols, 0),
            "end": get(cols, 1),
            "subject": get(cols, 3),
            "room": get(cols, 5)
        })

finally:
    driver.quit()


# save timetable
with open("timetable.json", "w") as f:
    json.dump(timetable, f, indent=2)


print("Saved timetable.json")
