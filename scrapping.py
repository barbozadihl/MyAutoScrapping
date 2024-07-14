import pandas as pd
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
#The overrall goal is to automate the process of gathering a specific data and creating/updating the csv where it should be stored.

df_csv = "yumm_datasheets.csv"
#Basically cheking if the file actually exists, if not, creates it.
try:
    existing_df = pd.read_csv(df_csv)
except FileNotFoundError:
    # Create an empty DataFrame if the CSV doesn't exist yet
    existing_df = pd.DataFrame(columns=["replace :) with your columns"])


#Using Selenium to open an anon tab on chrome
service = Service()
options = webdriver.ChromeOptions()
driver = Driver(
        browser="chrome",
        uc=True,
        headless2=False,
        incognito=True,
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36 AVG/112.0.21002.139",
        do_not_track=True,
        undetectable=True
    )

base_url = "URL_HERE/?pag="
#I chose to leave "/?pag=" because often I need to scrappe more than one page and rerunning the script manually becomes time consuming
n_pages = 1 #(replace with the actual number of pages )
for i in range(1, n_pages + 1):
    url = base_url + str(i)
    driver.get(url)


    #time.sleep(10) (this is to avoid spamming)

  #from here on its pretty straight forward what the code is doing, in this example, gathering every h3 element. 
    h3_elements = driver.find_elements(By.TAG_NAME, "h3")
    for h3 in h3_elements:
        values = h3.text.strip().split("\n") #each element is split into a cell on the table, iterating each column; this might not work properly if the website has disorganized html
        print(f"Extracted values: {values}")
        if len(values) == 5:
            existing_df.loc[len(existing_df)] = values
        else:
            print(f"Skipping row with mismatched columns: {values}")
          
    driver.quit()
    print(existing_df)
    existing_df.to_csv(df_csv, index=False)
