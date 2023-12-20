##############################################
#   Image Scraper (ver.ar.mou.1.0.0)
#   Created By :
#   Arman Sharker - AUST_CSE_40
#   It's just a prototype version of
#   the image scraper... Don't expect much.
#   Credit the owner if possible... ty... :D
##############################################

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import requests
from urllib.parse import urlparse
import time
from selenium.webdriver.common.by import By

opt = webdriver.ChromeOptions()
opt.add_argument('--incognito')
opt.add_argument('--start-maximized')
opt.add_argument('--disable-application-cache')
opt.add_argument('--aggressive-cache-discard')
webdriver_path = "F:/thesis/imageScraperTest01/chromedriver.exe"
svc = Service(webdriver_path)
driver = webdriver.Chrome(service=svc, options=opt)
download_folder = "F:/thesis/imageScraperTest01/scrapedImages/"
os.makedirs(download_folder, exist_ok=True)
driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})
skipInitial = 0
skipEnd = 0
rowCount = 5
data = pd.read_csv("websiteURLs.csv", skiprows=range(skipInitial, skipEnd), nrows=rowCount)
URLs = list(data['URLs'])
for URL in URLs:
    print(URL)
for URL in URLs:
    try:
        driver.get(URL)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
        image_elements = driver.find_elements(By.TAG_NAME, "img")
        image_count = 0
        for image_element in image_elements:
            image_url = image_element.get_attribute("src")
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_filename = os.path.basename(urlparse(image_url).path)
                    image_path = os.path.join(download_folder, image_filename)
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    image_count += 1
                    print(f"Image {image_count}: {image_url}")
                    time.sleep(1)
    except Exception as e:
        print(e)
        continue
driver.quit()
print(f"Downloaded {image_count} images to {download_folder}.")
