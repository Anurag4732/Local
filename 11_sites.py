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
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/samsung_scrape', convert_unicode=True)


today = date.today()
dat = today.strftime("%d-%m-%Y")
now = datetime.now()
cur_time = now.strftime("%-I:00 %p")

def vasanth_and_co(engine):
    from datetime import datetime
    from selenium.webdriver.common.keys import Keys
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'Vasanth and Co'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//div[@class = 'label-stock label label-success ']").is_displayed:
                return("No Stock Avaiable")       
        except:
            return("Stock Avaiable")
                
       

    for i in dfs.itertuples():
        driver.get('https://vasanthandco.in/')  # Open home page where we search the 
        time.sleep(3)
        try:
            name = re.sub('-',' ',i[4].split('.in/')[1])
            driver.find_element_by_xpath('//input[@class = "autosearch-input form-control"]').send_keys(name)
            driver.find_element_by_xpath('//button[@class="button-search btn btn-default btn-lg"]').click()
            time.sleep(3)

            try:
                product_name = driver.find_element_by_xpath("//div[@class = 'caption']//h4//a").text
            except:
                product_name = "Not Available"

            try:
                Discounted_Price = float(re.sub('[₹,]','',driver.find_element_by_xpath("//span[@class = 'price-new']").text)) #d_price
            except:
                Discounted_Price = "Not Available"

            stock = out_of_stock()

            try:
                Price = float(re.sub('[₹,]', '',driver.find_element_by_xpath("//span[@class = 'price-old']").text))  # mrp  
            except:
                Price = "Not Available"

            try:
                discount = driver.find_element_by_xpath("//span[@class = 'label-product label-sale']").text   
            except:
                discount = "Not Available"

            df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                                'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
            df2.to_sql('Scrapped_data_1', con=engine,
                       if_exists='append', index=False)
        except Exception as e:
            print(e)
            pass
    driver.close()

def kohinoor(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'kohinoor'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//div[@class = 'title-product']").is_displayed:
                if driver.find_element_by_xpath("//div[@class = 'stock']").text == 'Availability: Sold Out':
                    return("No Stock Avaiable")
                else:
                    return("Stock Avaiable")
        except:
             return("Not Avaiable")
            
                

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//div[@class = 'title-product']").text
        except:
            product_name = "Not Available"

        try:
            Discounted_Price = float(re.sub(',','',driver.find_element_by_xpath("//span[@class = 'price-new']").text.split()[-1]))
        except:
            Discounted_Price = "Not Available"

        stock = out_of_stock()

        try:
            Price = float(re.sub(',','',driver.find_element_by_xpath("//span[@class = 'price-old']").text.split('MRP')[1])) 
        except:
            Price = "Not Available"

        try:
            discount = driver.find_element_by_xpath("//span[@class = 'label-product label-sale new-sale-label']").text.split()[0]
        except:
            discount = "Not Available"
            
            
        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)
    driver.close()
                   
def Harsha_India(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'Harsha India'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//span[@style = 'text-transform: none;']").is_displayed:
                if driver.find_element_by_xpath("//*[contains(text(), 'Available Quantity:  ')]").text == 'Available Quantity: Out of Stock':
                    return("No Stock Avaiable")
                else:
                    return("Stock Avaiable")
        except:
            return("Not Avaiable")

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//span[@style = 'text-transform: none;']").text
        except:
            product_name = "Not Available"

        try:
            Discounted_Price = float(re.sub(',','',driver.find_element_by_xpath("//span[@class = 'price-new']").text.split()[1]))
        except:
            Discounted_Price = "Not Available"

        stock = out_of_stock()

        try:
            Price = float(re.sub(',','',driver.find_element_by_xpath("//span[@class = 'price-old']").text.split()[1])) 
        except:
            Price = "Not Available"

        try:
            discount = driver.find_element_by_xpath("//div[@class = 'product-label-special label']").text
        except:
            discount = "Not Available"
            
            
        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)
    driver.close()



def Unilet_stores(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'Unilet Stores'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if  driver.find_element_by_xpath("//h1[@class = 'product_title entry-title']").is_displayed:
                if driver.find_element_by_xpath("//p[@class = 'stock']").text == 'In Stock':
                    return("Stock Avaiable")
                elif driver.find_element_by_xpath("//p[@class = 'stock']").text == 'Out of stock':
                    return("No Stock Avaiable")
                elif driver.find_element_by_xpath("//p[@class = 'stock']").text == 'Few in stock':
                    return("Low Stock Avaiable")
                else:
                    return('Not Avaiable')
        except:
            return("Not Avaiable")

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//h1[@class = 'product_title entry-title']").text
        except:
            product_name = "Not Available"

        stock = out_of_stock()

        try:
            l = []
            for i in driver.find_element_by_xpath("//p[@class = 'price']//span[@class = 'woocommerce-Price-amount amount']"):
                try:
                    l.append(float(re.sub('[₹,]','',i.text)))
                except:
                    l.append('Not Available')

            Discounted_Price = l[0]
            Price = l[1]

        except:
            Discounted_Price = 'Not Available'
            Price = "Not Available"

        try:
            discount = driver.find_element_by_xpath("//p[@class = 'price']//ins[@class = 'pertextt']").text.split()[0]
        except:
            discount = "Not Available"

        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)
    driver.close()

def Pai_international(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'Pai_international'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//div[@class = 'ctl_aboutbrand']//h1").is_displayed:
                try:
                    if driver.find_element_by_xpath("//div[@class = 'instock']//span").is_displayed:
                        return("Stock Avaiable")
                except:
                    return('No Stock Avaiable')  # ("//div[@class = 'outofstock']//span")
        except:
            return('Not Avaiable')
        
                
       

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//div[@class = 'ctl_aboutbrand']//h1").text
        except:
            product_name = "Not Available"

        try:
            Discounted_Price = float(re.sub('[INR,]','',driver.find_element_by_xpath('//span[@class = "offer"]').text.split()[1]))
        except:
            Discounted_Price = "Not Available"

        stock = out_of_stock()

        try:
            Price = float(re.sub('[INR,]','',driver.find_element_by_xpath("//span[@class = 'mrp']").text.split()[1]))  
        except:
            Price = "Not Available"

        try:
            discount = driver.find_element_by_xpath("//b[@class = 'lb5']").text   
        except:
            discount = "Not Available"

        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)

    driver.close()
            
                   
def Bajaj_electronics(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'Bajaj_electronics'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//div[@class = 'col-lg-6 col-md-12 content']//h4").is_displayed:
                try:
                    if driver.find_element_by_xpath("//div[@class = 'mt10']").is_displayed:
                        return('No Stock Avaiable')
                except:
                    return("Stock Avaiable")
        except:
            return('Not Avaiable')
        
                
       

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//div[@class = 'col-lg-6 col-md-12 content']//h4").text
        except:
            product_name = "Not Available"

        try:
            Discounted_Price = float(re.sub(',','',driver.find_element_by_xpath("//div[@class = 'priceDetails']//h3").text.split()[1]))     # d_price '₹ 5,780 Inclusive of all taxes'
        except:
            Discounted_Price = "Not Available"

        stock = out_of_stock()
        try:
            Price = float(re.sub('[₹,]','',driver.find_element_by_xpath("//span[@class = 'offer']").text))
        except:
            Price = "Not Available"

        try:
            discount = driver.find_element_by_xpath("//span[@class = 'ProductDiscount']").text.split()[0]    # '21% off'
        except:
            discount = "Not Available"

        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)
                   
    driver.close() 

def sargam(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'Sargam'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
           if driver.find_element_by_xpath("//span[@class = 'base']").is_displayed: 
                try:
                    if driver.find_element_by_xpath("//div[@class = 'stock available']").is_displayed:
                        return("Stock Avaiable")
                except:
                    return("No Stock Avaiable")
        except:
            return('Not Avaiable')

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//span[@class = 'base']").text
        except:
            product_name = "Not Available"

        try:
            Discounted_Price = float(re.sub('[₹,]', '',driver.find_element_by_xpath("//span[@class = 'special-price']").text))
        except:
            Discounted_Price = "Not Available"
            
        stock = out_of_stock()
        
        try:
            Price = float(re.sub('[₹,]', '',driver.find_element_by_xpath("//span[@class = 'old-price']").text)) 
        except:
            Price = "Not Available"
            
        try:
            discount = driver.find_element_by_xpath("//span[@class= 'discount-percent']").text
        except:
            discount = "Not Available"

        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)
    driver.close() 
    
    
def Adishware_store(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'Adishware_store'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//div[@class = 'ctl_aboutbrand']//h1").is_displayed:
                try:
                    if driver.find_element_by_xpath("//div[@class = 'instock']").is_displayed:
                        return('Stock Avaiable')
                except:
                    return('No Stock Avaiable')
        except:
            return('Not Avaiable')

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//div[@class = 'ctl_aboutbrand']//h1").text
        except:
            product_name = "Not Available"
            
        stock = out_of_stock()

        try:
            Discounted_Price = float(re.sub('[INR,]', '',driver.find_element_by_xpath("//span[@class = 'offer']").text))
        except:
            Discounted_Price = "Not Available"

        try:
            Price = float(re.sub('[INR,]','',driver.find_element_by_xpath("//span[@class = 'mrp']").text)) 
        except:
            Price = "Not Available"
            
        try:
            discount = driver.find_element_by_xpath("//span[@class = 'offer_block']").text
        except:
            discount = "Not Available"

        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)

    driver.close()        
    
def Sathya(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'Sathya'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//h1[@class = 'pd-name pd-name-sm']").is_displayed:
                try:
                    if driver.find_element_by_xpath("//div[@class = 'col flex-grow-1']").is_displayed:
                        return("Stock Avaiable")
                except:
                    return("No Stock Avaiable")
        except:
            return('Not Avaiable')

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//h1[@class = 'pd-name pd-name-sm']").text
        except:
            product_name = "Not Available"

        try:
            Discounted_Price = float(re.sub('[₹,]', '',driver.find_element_by_xpath("//div[@class = 'pd-price pd-price--offer']").text))
        except:
            Discounted_Price = "Not Available"

        stock = out_of_stock()

        try:
            Price = float(re.sub('[₹,]', '',driver.find_element_by_xpath("//span[@class = 'pd-oldprice']").text)) 
        except:
            Price = "Not Available"

        try:
            discount = driver.find_element_by_xpath("//span[@class = 'pd-saving-percent']").text
        except:
            discount = "Not Available"

        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)
    driver.close()                

def Aditya_vision(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'Aditya_vision'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//h2[@class = 'page-title']").is_displayed:
                try:
                    if driver.find_element_by_xpath("//div[@class = 'product-info-stock-sku']//span").text == 'Out of stock':
                        return("No Stock Avaiable")
                    else:
                        return("Stock Avaiable")
                except:
                    return("Not Avaiable")
        except:
            return('Not Avaiable')

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//h2[@class = 'page-title']").text
        except:
            product_name = "Not Available"

        try:
            Discounted_Price = float(re.sub(',','',driver.find_element_by_xpath("//span[@class = 'special-price']").text.split('₹')[1]))
        except:
            Discounted_Price = "Not Available"

        stock = out_of_stock()

        try:
            Price = float(re.sub(',','',driver.find_element_by_xpath("//span[@class = 'old-price']").text.split('₹')[1]))
        except:
            Price = "Not Available"

        try:
            discount = driver.find_element_by_xpath("//span[@class = 'perc-cls']").text.split()[1]
        except:
            discount = "Not Available"
            
            
        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)
    driver.close() 
    
    
def myg(engine):
    from datetime import datetime
    import re
    query = """
    select Platform,Category,id,Url from url where Platform = 'myg'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//h1[@class = 'ty-product-block-title']").is_displayed:
                try:
                    if driver.find_element_by_xpath("//span[@class = 'ty-qty-out-of-stock ty-control-group__item']").is_displayed:
                        return("No Stock Avaiable")
                except:
                    return("Stock Avaiable")
        except:
            return('Not Avaiable')

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//h1[@class = 'ty-product-block-title']").text
        except:
            product_name = "Not Available"

        try:
            Discounted_Price = float(re.sub('[₹,]','',driver.find_element_by_xpath("//div[@class = 'ty-product-block__price-actual']").text))
        except:
            Discounted_Price = "Not Available"

        stock = out_of_stock()

        try:
            Price = float(re.sub('[₹,]','',driver.find_element_by_xpath("//span[@class = 'ty-strike']").text))
        except:
            Price = "Not Available"

        try:
            discount = re.sub('[()]','',driver.find_element_by_xpath("//span[@class = 'ty-list-price ty-save-price ty-nowrap']").text).split()[-1]
        except:
            discount = "Not Available"
            
            
        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)
    driver.close() 
    





f1 = multiprocessing.Process(target=vasanth_and_co, args=[engine])
f2 = multiprocessing.Process(target=kohinoor, args=[engine])
f3 = multiprocessing.Process(target=Harsha_India, args=[engine])
f4 = multiprocessing.Process(target=Unilet_stores, args=[engine])
f5 = multiprocessing.Process(target=Pai_international, args=[engine])
f6 = multiprocessing.Process(target=Bajaj_electronics, args=[engine])
f7 = multiprocessing.Process(target=Sargam, args=[engine]) 
f8 = multiprocessing.Process(target=Adishware_store, args=[engine])
f9 = multiprocessing.Process(target=Sathya, args=[engine])
f10 = multiprocessing.Process(target=Aditya_vision, args=[engine])
f11 = multiprocessing.Process(target=myg, args=[engine])
#################
f1.start()
f2.start()
f3.start()
f4.start()
f5.start()
f6.start()
f7.start()
f8.start()
f9.start()
f10.start()
f11.start()
##############
f1.join()
f2.join()
f3.join()
f4.join()
f5.join()
f6.join()
f7.join()
f8.join()
f9.join()
f10.join()
f11.join()

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
