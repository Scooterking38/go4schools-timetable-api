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

homework_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Homework')]"))
)

driver.execute_script("arguments[0].click();", homework_link)

homework_rows = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.table tbody tr"))
)

homework = []

for row in homework_rows:
    cols = row.find_elements(By.TAG_NAME, "td")

    homework.append({
        "due": cols[1].text,
        "subject": cols[2].text.split("\n")[0],
        "task": cols[3].text.split("\n")[0],
        "status": cols[4].text,
        "grade": cols[5].text,
        "set": cols[6].text.split("\n")[0],
        "teacher": cols[6].text.split("\n")[1] if "\n" in cols[6].text else ""
    })

driver.quit()

# save JSON
with open("timetable.json", "w") as f:
    json.dump(timetable, f, indent=2)
with open("homework.json", "w") as f:
    json.dump(homework, f, indent=2)

print("Saved homework.json")
print("Saved timetable.json")
