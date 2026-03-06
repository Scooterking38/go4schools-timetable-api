from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json

# enable headless mode
options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(
    service=Service(GeckoDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)

driver.get("https://www.go4schools.com/sso/account/login?site=Student")

# username
username = wait.until(
    EC.presence_of_element_located((By.ID, "usernameInput"))
)
username.send_keys(os.environ["USERNAME"])

# password
password = driver.find_element(By.ID, "passwordInput")
password.send_keys(os.environ["PASSWORD"])
password.send_keys(Keys.RETURN)

# wait for timetable rows
rows = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.ghost-content"))
)

timetable = []

for row in rows:
    cols = row.find_elements(By.XPATH, "./th|./td")

    start = cols[0].text
    end = cols[1].text
    subject = cols[3].text
    room = cols[5].text

    timetable.append({
        "start": start,
        "end": end,
        "subject": subject,
        "room": room
    })

# save JSON
with open("timetable.json", "w") as f:
    json.dump(timetable, f, indent=2)

driver.quit()
