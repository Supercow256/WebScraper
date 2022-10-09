import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# get user input
newUsedInput = input("Please enter a number \n0: New & Used Cars \n1: New & Certified Cars \n2: New Cars \n3: Used Cars \n4: Certified Cars\n")
if newUsedInput != "0" and newUsedInput != "1" and newUsedInput != "2" and newUsedInput != "3" and newUsedInput != "4":
    newUsedInput = input("Please Pick one of the options\n")
makeInput = input("Please enter a Make (keep blank for all): ")
modelInput = input("Please enter a Model (keep blank for all): ")
priceInput = input("Please enter one of the following max prices (with the dollar sign and comma included)\n"
                   "$2000, $4000, $6000, $8000, $10,000, $15,000, $20,000, $25,000, $30,000, $35,000, $40,000, $45,000, $50,000, $60,000\n"
                   "$70,000, $80,000, $90,000, $100,000, $125,000, $150,000, $175,000\n")
distanceInput = input("Please enter one of the following max miles\n"
                   "10, 20, 30, 40, 50, 75, 100, 150, 200, 250, 500, all miles\n")
zipInput = input("Please enter your zipcode: ")

driver = webdriver.Chrome(executable_path='C:/Users/misyu/Downloads/chromedriver_win32/chromedriver.exe')
driver.get('https://www.cars.com/')
# get dropdowns and elements
newUsedDropDown = driver.find_element(By.NAME, "stock_type")
makeDropDown = driver.find_element(By.NAME, "makes[]")
modelDropDown = driver.find_element(By.NAME, "models[]")
PriceDropDown = driver.find_element(By.NAME, "list_price_max")
distanceDropDown = driver.find_element(By.NAME, "maximum_distance")
zipInputField = driver.find_element(By.NAME, "zip")
# check if tag is <select>
# dd = Select(newUsedDropDown)

# select value for dropdown
Select(newUsedDropDown).select_by_index(newUsedInput)
if makeInput != "":
    Select(makeDropDown).select_by_visible_text(makeInput)
if modelInput != "":
    Select(modelDropDown).select_by_visible_text(modelInput)
Select(PriceDropDown).select_by_visible_text(priceInput)
Select(distanceDropDown).select_by_visible_text(distanceInput + " miles")
# click on input field
zipInputField.click()
# type into input field
zipInputField.send_keys(zipInput)
# set text/ click enter
zipInputField.send_keys(Keys.RETURN)

# FORM IS COMPLETE NOW SCRAPE
# without sleep there are error, does the page need time to load results?

time.sleep(1)
# create arrays
carType = []
carPrice = []

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
carList = soup.find(id="vehicle-cards-container")
carElements = carList.find_all("div", class_="vehicle-card")
for car in carElements:
    title = car.find("h2", class_="title").text
    price = car.find("span", class_="primary-price").text
    carType.append(title)
    carPrice.append(price)


# Create and display DataFrame
df = pd.DataFrame({
    f'Car':carType,
    f'Price': carPrice
    })
df.to_csv('cars.csv', index=False, encoding='utf-8')

# if exit code is 0, everything worked correctly