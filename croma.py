from datetime import date,datetime
from selenium import webdriver
import pandas as pd
from time import sleep
import sqlalchemy
import pandas as pd
import pymysql
import time
import numpy as np
import re
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path=r"C:\Users\Anurag\Downloads\chromedriver_win32\chromedriver.exe")

def info():
    def out_of_stock():
            try:
                if driver.find_element_by_xpath("//h3[contains(text(),'Sold Out')]").is_displayed:
                    return("Stock Not Available")
            except:
                return("Stock Available")


    try:
        product_name = driver.find_element_by_xpath("//small[@class = 'product_name_small']/h1").text
    except:
        product_name = "Not Available"

    stock = out_of_stock()

    try:
        Discounted_Price = driver.find_element_by_xpath("//span[@class = 'pdpPrice']").text
        Discounted_Price = float(re.sub('[₹,]', "", Discounted_Price))
    except:
        Discounted_Price = "Not Available"

    try:
        Price = driver.find_element_by_xpath("//span[@class = 'pdpPriceMrp']").text
        Price = float(re.sub('[₹,]', "", Price))
    except:
        Price = "Not Available"
    try:
        discount = round(((Price - Discounted_Price) / Price) * 100)
        discount = (str(discount) + "%")
    except:
        discount = (str(0) + "%")

    return(product_name, stock, Discounted_Price, Price, discount)

# Input
link = 'https://www.croma.com/samsung-8-kg-fully-automatic-front-loading-washing-machine-ww80j54e0iw-tl-white-/p/217483'
driver.get(link)
time.sleep(5)

if driver.current_url == 'https://www.croma.com/':
    try:
        unique_id = 'WW80J54E0IW'  # i[3]
        driver.find_element_by_xpath("//input[@class = 'form-control js-site-search-input search-box ui-autocomplete-input']").send_keys(unique_id)
        driver.find_element_by_xpath("//button[@class = 'btn btn-link js_search_button group2 glphicon']").send_keys(Keys.ENTER) # click for search
        time.sleep(10)
        if driver.find_element_by_xpath("//div[@class = 'pagination-bar-results ']").text == '1 Products found':
            driver.find_element_by_xpath('//a[@class =  "product__list--name"]').click()
            time.sleep(10)
            product_name, stock, Discounted_Price, Price, discount = info()
        else:
            print('Unique product not found')
            pass
            
    except:
        product_name = 'Not Available'
        stock = 'Not Available'
        Discounted_Price = 'Not Available'
        Price = 'Not Available'
        discount = 'Not Available'
        pass
else:
    try:
        product_name, stock, Discounted_Price, Price, discount = info()
    except:
        product_name = 'Not Available'
        stock = 'Not Available'
        Discounted_Price = 'Not Available'
        Price = 'Not Available'
        discount = 'Not Available'
        pass  
    
print(product_name, stock, Discounted_Price, Price, discount)
