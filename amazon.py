import mysql.connector
import numpy as np
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from time import sleep
import sqlalchemy
import pandas as pd
import pymysql
import re
import time
import datetime
import multiprocessing
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
start_time = datetime.now()
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument("--incognito")
# today = date.today()
dat = '8/8/2020'

# now = datetime.now()
cur_time = '11:00 AM'

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/samsung_scrape', convert_unicode=True)
driver = webdriver.Chrome(r'C:\Users\Anurag\Downloads\chromedriver_win32\chromedriver')

def Amazon_scrap(engine,pin_):
#     chrome_options = Options()
#     chrome_options.add_argument("--incognito")
#     from datetime import datetime
    query = """
    select Platform,Category,id,Url from url where Platform = 'amazon'
    """
    dfs = pd.read_sql_query(query, engine)

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//*[contains(text(), 'Only 1 left in stock.')]").is_displayed():
                return("Low Stock Available")
        except:
            pass
        try:
            if driver.find_element_by_xpath("//*[contains(text(), 'Only 2 left in stock.')]").is_displayed():
                return("Low Stock Available")
        except:
            pass
        try:
            if driver.find_element_by_xpath("//*[contains(text(), 'In stock.')]").is_displayed():
                return("Stock Available")
        except:
            return("Stock Not Available")
#     driver = webdriver.Chrome(chrome_options=chrome_options,
#                               executable_path='/home/qdgrees/Downloads/chromedriver')

    for i in dfs.itertuples():
        Product_MRP = []
        Product_Selling_Price = []
        Product_discount = []
        Seller = []
        asin_code = []
        seller_code = []
        driver.get(i[4])
        sleep(2)
        
        pin_code = pin_
        driver.find_element_by_xpath("//a[@class = 'nav-a nav-a-2 a-popover-trigger a-declarative']").click()
        time.sleep(5)
        driver.find_element_by_xpath("//input[@class = 'GLUX_Full_Width a-declarative']").send_keys(6*Keys.BACKSPACE)
        driver.find_element_by_xpath("//input[@class = 'GLUX_Full_Width a-declarative']").send_keys(pin_code)
        driver.find_element_by_xpath("//span[@id='GLUXZipUpdate']").click()
        time.sleep(10)
        
        stock = out_of_stock()
        try:
            MRP = driver.find_element_by_xpath(
                "//span[@class='priceBlockStrikePriceString a-text-strike']")
            MRP = float(re.sub('[₹,]', "", MRP.text))
        except:
            MRP = "Not Available"
        try:
            try:
                try:  # new more(mulli seller)
                    if driver.find_element_by_xpath("//div/div[@class='a-section a-spacing-small a-spacing-top-small']").is_displayed():
                        s_page = driver.find_element_by_xpath(
                            "//div/div[@class='a-section a-spacing-small a-spacing-top-small']/a").click()
                        sleep(2)
                        ###################  NEW   ###########################
                        try:
                            for var in driver.find_elements_by_xpath("//span[@class='a-size-medium a-text-bold']//a"):
                                temp = var.get_attribute('href')
                                try:
                                    asin_code.append(temp.split(
                                        'asin=')[1].split('&')[0])
                                except:
                                    asin_code.append('Not Available')
                                try:
                                    seller_code.append(
                                        temp.split('seller=')[1])
                                except:
                                    seller_code.append('Not Available')
                        except:
                            asin_code.append('Not Available')
                            seller_code.append('Not Available')
                        ########################################################

                        try:
                            product_name = driver.find_element_by_xpath(
                                "//h1[@class='a-size-large a-spacing-none']").text
                        except:
                            product_name = "Not Available"

                        seller_names = driver.find_elements_by_xpath(
                            "//div[@class='a-column a-span2 olpSellerColumn']/h3/span/a")
                        for name in seller_names:
                            Seller.append(name.text)
                        try:
                            Disc_Prices = driver.find_elements_by_xpath(
                                "//span[@class='a-size-large a-color-price olpOfferPrice a-text-bold']/span")
                            for Disc_Price in Disc_Prices:
                                Disc_Price = float(
                                    re.sub('[₹,]', "", Disc_Price.text))
                                Product_Selling_Price.append(Disc_Price)
                        except:
                            Product_Selling_Price.append("Not Available")

                        try:
                            for d in Product_Selling_Price:
                                discount = round(((MRP - d) / MRP) * 100)
                                discount = (str(discount) + "%")
                                Product_discount.append(discount)
                        except:
                            discount = (str(0) + "%")
                            Product_discount.append(discount)

                        df = pd.DataFrame({'Product_Selling_Price': pd.Series(Product_Selling_Price), 'asin_code': pd.Series(asin_code), 'seller_code': pd.Series(seller_code),
                                           'Product_discount': pd.Series(Product_discount), 'Seller': pd.Series(Seller)})
                        df['Product_MRP'] = MRP
                        df['Product_name'] = product_name
                        df['Date'] = dat
                        df['Time'] = cur_time
                        df['Product_Category'] = i[2]
                        df['Product_platform'] = i[1]
                        df['Product_availability'] = stock
                        df['Product_id'] = i[3]
                        df['Product_Urls'] = i[4]
                        df['pin_code'] = pin_code

                        df = df[['Date', 'Time', 'Product_Category', 'Product_platform',
                                 'Product_name', 'Product_id',
                                 'Product_MRP', 'Product_Selling_Price',
                                 'Product_discount', 'Seller', 'Product_availability','pin_code', 'Product_Urls', 'asin_code', 'seller_code']]
                        print(df)
                except:  # these seller(only one)
                    if driver.find_element_by_xpath("//*[contains(text(), 'Available from')]").is_displayed():
                        s_page = driver.find_element_by_xpath(
                            "//div[@id ='availability']/span/a").click()
                        sleep(2)

                        ##################  NEW  #####################
                        try:
                            for var in driver.find_elements_by_xpath("//span[@class='a-size-medium a-text-bold']//a"):
                                temp = var.get_attribute('href')
                                try:
                                    asin_code_var = temp.split(
                                        'asin=')[1].split('&')[0]
                                except:
                                    asin_code_var = 'Not Available'
                                try:
                                    seller_code_var = temp.split('seller=')[1]
                                except:
                                    seller_code_var = 'Not Available'
                        except:
                            asin_code_var = 'Not Available'
                            seller_code_var = 'Not Available'
                        ################################################
                        try:
                            product_name = driver.find_element_by_xpath(
                                "//h1[@class='a-size-large a-spacing-none']").text
                        except:
                            product_name = "Not Available"
                        try:
                            seller_names = driver.find_element_by_xpath(
                                "//div[@class='a-column a-span2 olpSellerColumn']/h3/span/a").text
                        except:
                            seller_names = "Not Available"

                        try:
                            Disc_Prices = driver.find_element_by_xpath(
                                "//span[@class='a-size-large a-color-price olpOfferPrice a-text-bold']/span")
                            Disc_Price = float(
                                re.sub('[₹,]', "", Disc_Prices.text))
                        except:
                            Disc_Price = "Not Available"
                            discount = (str(0) + "%")

                        df = pd.DataFrame({'Product_Selling_Price': Disc_Price, 'asin_code': asin_code_var, 'seller_code': seller_code_var,
                                           'Product_discount': discount, 'Seller': seller_names}, index=[0])
                        df['Product_MRP'] = MRP
                        df['Product_name'] = product_name
                        df['Date'] = dat
                        df['Time'] = cur_time
                        df['Product_Category'] = i[2]
                        df['Product_platform'] = i[1]
                        df['Product_availability'] = "Stock Available"
                        df['Product_id'] = i[3]
                        df['Product_Urls'] = i[4]
                        df['pin_code'] = pin_code

                        df = df[['Date', 'Time', 'Product_Category', 'Product_platform',
                                 'Product_name', 'Product_id',
                                 'Product_MRP', 'Product_Selling_Price',
                                 'Product_discount', 'Seller', 'Product_availability','pin_code', 'Product_Urls', 'asin_code', 'seller_code']]
                        print(df)

            except:  # single seller

                try:
                    product_name = driver.find_element_by_xpath(
                        "//h1[@id='title']/span").text
                except:
                    product_name = "Not Available"

                try:
                    Discounted_Price = driver.find_element_by_xpath(
                        "//td[@class='a-span12']/span")
                    Discounted_Price = float(
                        re.sub('[₹,]', "", Discounted_Price.text))
                except:
                    Discounted_Price = "Not Available"

                try:
                    asin_code_var = i[4].split('dp/')[1].split('/ref')[0]
                except:
                    asin_code_var = 'Not Available'
                try:
                    temp = driver.find_elements_by_xpath(
                        "//div[@id= 'merchant-info']//a")[0].get_attribute('href')
                    seller_code_var = temp.split('seller=')[1].split('&')[0]
                except:
                    seller_code_var = 'Not Available'

                try:
                    discount = round(((MRP - Discounted_Price) / MRP) * 100)
                    discount = (str(discount) + "%")
                except:
                    discount = (str(0) + "%")

                Seller_all = driver.find_element_by_xpath(
                    "//*[contains(text(), 'Sold by')]").text
                b = re.split(' ', Seller_all)
                c = b[2:-4]
                Seller_only = " ".join(c)

                df = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2],
                                   'Product_platform': i[1], 'Product_name': product_name,
                                   'Product_id': i[3], 'Product_MRP': MRP,
                                   'Product_Selling_Price': Discounted_Price,'pin_code':pin_code,
                                   'Product_discount': discount, 'Seller': Seller_only,
                                   'Product_availability': stock, 'Product_Urls': i[4], 'asin_code': asin_code_var, 'seller_code': seller_code_var}, index=[0])
                print(df)
        except:  # not availabel
            try:
                product_name = driver.find_element_by_xpath(
                    "//h1[@id='title']/span").text
            except:
                product_name = "Not Available"
            try:
                Discounted_Price = driver.find_element_by_xpath(
                    "//td[@class='a-span12']/span")
                Discounted_Price = float(
                    re.sub('[₹,]', "", Discounted_Price.text))
            except:
                Discounted_Price = "Not Available"
            try:
                asin_code_var = i[4].split('dp/')[1].split('/ref')[0]
            except:
                asin_code_var = 'Not Available'

            df = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2],
                               'Product_platform': i[1], 'Product_name': product_name,
                               'Product_id': i[3], 'Product_MRP': MRP,
                               'Product_Selling_Price': Discounted_Price,'pin_code':pin_code,
                               'Product_discount': str(0) + "%", 'Seller': "Not Available",
                               'Product_availability': "Stock Not Available", 'Product_Urls': i[4], 'asin_code': asin_code_var, 'seller_code': "Not Available"}, index=[0])
            print(df)

#     driver.close()
    
for pin_ in [500001, 110052, 560034, 700001]:
    Amazon_scrap(engine, pin_)
