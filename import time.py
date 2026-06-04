import time
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ================================
# 🔥 SETUP DRIVER (HEADLESS FOR COLAB)
# ================================
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--no-sandbox") # Required for running in Colab
options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
options.add_argument("--disable-gpu") # Disable GPU hardware acceleration
options.add_argument("--window-size=1920,1080") # Set a consistent window size
options.add_argument("--user-data-dir=/tmp/user-data") # Use a temporary user data directory
options.binary_location = "/usr/bin/google-chrome" # Specify the Chrome binary location (after installing google-chrome-stable)

# Use ChromeDriverManager to manage the chromedriver executable
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), # Let webdriver_manager handle chromedriver
    options=options
)

# ================================
# 🔗 OPEN UPWORK
# ================================
search_url = "https://www.upwork.com/nx/jobs/search/?q=data%20analyst"
driver.get(search_url)

# input("👉 Login karo manually, then press ENTER...") # Manual login is not possible in headless mode

# Wait for the page to load and potentially handle any pop-ups if necessary
time.sleep(5)

data = []

# ================================
# 🔁 LOOP PAGES
# ================================
for page in range(3):

    time.sleep(random.uniform(4, 7))

    jobs = driver.find_elements(By.XPATH, "//section[contains(@class,'job-tile')]")

    for job in jobs:

        # -------------------------
        # BASIC INFO
        # -------------------------
        try:
            title = job.find_element(By.XPATH, ".//h3").text
        except:
            title = ""

        try:
            link = job.find_element(By.XPATH, ".//a").get_attribute("href")
        except:
            link = ""

        # -------------------------
        # 🔥 OPEN JOB DETAIL PAGE
        # -------------------------
        description = ""
        skills = []
        budget = ""
        client_spent = ""
        hire_rate = ""
        proposals = ""
        location = ""

        if link:
            try:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)

                time.sleep(random.uniform(5, 8))

                # Description
                try:
                    description = driver.find_element(By.XPATH, "//div[contains(@class,'description')]").text
                except:
                    pass

                # Skills
                try:
                    skill_elements = driver.find_elements(By.XPATH, "//span[contains(@class,'skill')]")
                    skills = [s.text for s in skill_elements]
                except:
                    pass

                # Budget
                try:
                    budget = driver.find_element(By.XPATH, "//strong[contains(text(),'$')]").text
                except:
                    pass

                # Client details (TEXT BASED EXTRACTION)
                full_text = driver.find_element(By.TAG_NAME, "body").text.lower()

                if "spent" in full_text:
                    client_spent = "Yes"
                if "hire rate" in full_text:
                    hire_rate = "Yes"
                if "proposals" in full_text:
                    proposals = "Yes"

                # Location
                try:
                    location = driver.find_element(By.XPATH, "//span[contains(@class,'location')]").text
                except:
                    pass

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except:
                driver.switch_to.window(driver.window_handles[0])

        data.append({
            "project_title": title,
            "project_link": link,
            "description": description,
            "skills": ", ".join(skills),
            "budget": budget,
            "client_spent_flag": client_spent,
            "hire_rate_flag": hire_rate,
            "proposals_flag": proposals,
            "location": location
        })

    # NEXT PAGE
    try:
        next_btn = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
        driver.execute_script("arguments[0].click();", next_btn)
    except:
        break


driver.quit()

df = pd.DataFrame(data)
df.to_csv("upwork_pro_data.csv", index=False)

print("✅ DONE - upwork_pro_data.csv created")