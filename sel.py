import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 30)

driver.get("https://www.go4schools.com/sso/account/login?site=Student")

username = wait.until(
    EC.presence_of_element_located((By.ID, "usernameInput"))
)
username.send_keys(USERNAME)

password = driver.find_element(By.ID, "passwordInput")
password.send_keys(PASSWORD)
password.send_keys(Keys.RETURN)

rows = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.ghost-content"))
)

timetable = []

for row in rows:
    cols = row.find_elements(By.XPATH, "./th|./td")

    timetable.append({
        "start": cols[0].text,
        "end": cols[1].text,
        "subject": cols[3].text,
        "room": cols[5].text
    })

driver.quit()

# save JSON
with open("timetable.json", "w") as f:
    json.dump(timetable, f, indent=2)

print("Saved timetable.json")
