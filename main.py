import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)


URL = ("https://www.zillow.com/asheville-nc/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible"
       "%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A35.682396761279634%2C%22south%22%3A35.417032517424396%2C"
       "%22east%22%3A-82.36933344042967%2C%22west%22%3A-82.7332555595703%7D%2C%22filterState%22%3A%7B%22fr%22%3A%7B"
       "%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C"
       "%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22"
       "%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B"
       "%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A536684%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C"
       "%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A50779%2C"
       "%22regionType%22%3A6%7D%5D%2C%22usersSearchTerm%22%3A%22%22%7D")
#
Form_Url = "your googlesheets url"
headers = {
    "Accept-Language": "en-US,en;q=0.9,nl;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0.0.0 Safari/537.36",
}

response = requests.get(URL, headers=headers)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

# Get address of the property
addresses = soup.find_all("a", class_="property-card-link")

# Get the price of the properties
prices = soup.find_all("span", class_="iMKTKr")

# Form a list of all the prices
rents = [rent.text for rent in prices]

# List of the property addresses
property_addresses = [address.text for address in addresses if address.text != ""]

# A list of all the properties in the right format to allow client visit the url
property_links = ["https://www.zillow.com" + link.get("href") for link in addresses]

# Open the Google form in your Google sheet
driver.get(Form_Url)

# Fill out the form for every property
for i in range(len(rents)):
    sleep(2)
    property_rent = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                                  '1]/div/div[1]/input')
    property_rent.send_keys(rents[i])

    property_address = driver.find_element(By.XPATH,
                                           '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                           '1]/div/div[1]/input')
    property_address.send_keys(property_addresses[i])

    property_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                                  '1]/div/div[1]/input')
    property_link.send_keys(property_links[i])

    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
    sleep(3)
    driver.get(Form_Url)

driver.quit()
