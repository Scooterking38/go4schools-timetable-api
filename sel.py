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
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 30)


def get(cols, i):
    return cols[i].text if len(cols) > i else ""


try:
    driver.get("https://www.go4schools.com/sso/account/login?site=Student")

    username = wait.until(
        EC.presence_of_element_located((By.ID, "usernameInput"))
    )
    username.send_keys(USERNAME)

    password = driver.find_element(By.ID, "passwordInput")
    password.send_keys(PASSWORD)
    password.send_keys(Keys.RETURN)

    # wait for timetable rows to appear (ensures login finished)
    rows = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.ghost-content"))
    )

    timetable = []

    for row in rows:
        cols = row.find_elements(By.XPATH, "./th|./td")

        timetable.append({
            "start": get(cols, 0),
            "end": get(cols, 1),
            "subject": get(cols, 3),
            "room": get(cols, 5)
        })

    homework_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Homework')]"))
    )

    homework_link.click()

    homework_rows = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.table tbody tr"))
    )

    homework = []

    for row in homework_rows:
        cols = row.find_elements(By.TAG_NAME, "td")

        teacher_info = get(cols, 6).split("\n")

        homework.append({
            "due": get(cols, 1),
            "subject": get(cols, 2).split("\n")[0],
            "task": get(cols, 3).split("\n")[0],
            "status": get(cols, 4),
            "grade": get(cols, 5),
            "set": teacher_info[0] if teacher_info else "",
            "teacher": teacher_info[1] if len(teacher_info) > 1 else ""
        })

finally:
    driver.quit()


with open("timetable.json", "w") as f:
    json.dump(timetable, f, indent=2)

with open("homework.json", "w") as f:
    json.dump(homework, f, indent=2)

print("Saved timetable.json")
print("Saved homework.json")
