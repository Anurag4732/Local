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

## Fetching from db = 'samsung_scrape', table = 'url'
## Pushing into  db = 'samsung_scrape', table = 'Sentimark_review'

today = date.today()
dat = today.strftime("%d-%m-%Y")
now = datetime.now()
cur_time = now.strftime("%-I:00 %p")

def Amazon_sentimark(engine):
    query = """
    select Platform,Category,id,Url from url where Platform = 'Amazon'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(r'C:\Users\Anurag\Downloads\chromedriver_win32\chromedriver')
    
    for i in itertuples():
        url = i[4]  
        url = "/product-reviews/".join(url.split('/dp/'))
        driver.get(url)
        time.sleep(5)
        
        review_info = {
                'rating':[],
                'title':[],
                'sentiment_date':[],
                'review':[],
                'helpful':[]   
                }

        def review_(review_info):
            ## It's review and rating session that's we used len(rating) 
            try:
                number_rating_review = len(driver.find_elements_by_xpath('//*[@data-hook="review-star-rating"]'))
                if number_rating_review > 0:
                    for i in range(number_rating_review): 
                        try:
                            review_info['rating'].append(int(float(driver.find_elements_by_xpath('//*[@data-hook="review-star-rating"]')[i].get_attribute('class').split('a-star-')[1].split()[0])))
                        except:
                            review_info['rating'].append(0)  # If there is no rating
                        try:
                            review_info['title'].append(driver.find_elements_by_xpath('//a[@data-hook="review-title"]')[i].text)
                        except:
                            review_info['title'].append('Not Available')
                        try:
                            review_info['sentiment_date'].append(driver.find_elements_by_xpath('//span[@data-hook="review-date"]')[i].text.split('on ')[1])
                        except:
                            review_info['sentiment_date'].append('Not Available')
                        try:
                            review_info['review'].append(driver.find_elements_by_xpath('//span[@data-hook="review-body"]')[i].text)
                        except:
                            review_info['review'].append('Not Available')
                        try:
                            review_info['helpful'].append(int(driver.find_elements_by_xpath('//span[@data-hook="helpful-vote-statement"]')[i].text.split()[0]))
                        except:
                            review_info['helpful'].append(0)  # If nobody finds helpful
                    return(review_info)
                else:  ## When there is no review
                    review_info['rating'].append(0)
                    review_info['title'].append('Not Available')
                    review_info['sentiment_date'].append('Not Available')
                    review_info['review'].append('Not Available')
                    review_info['helpful'].append(0)
                    return(review_info)
            except:
                review_info['rating'].append('Not Available')
                review_info['title'].append('Not Available')
                review_info['sentiment_date'].append('Not Available')
                review_info['review'].append('Not Available')
                review_info['helpful'].append('Not Available')
                return(review_info)
                
        try:
            ## For this type only:- 18 global reviews | 3 global ratings
            ## Not for this      :- Showing 1-10 of 18 reviews
            total_review = int(driver.find_element_by_xpath("//div[@data-hook= 'cr-filter-info-review-rating-count']").text.split()[0])
        except:
            total_review = 0
        
        review_info = review_(review_info) # If there is no review, at that time it will also run for one time
        
        try:
            while driver.find_element_by_xpath("//li[@class = 'a-last']").is_displayed():
                driver.find_element_by_xpath("//li[@class = 'a-last']").click()
                time.sleep(5)
                review_info = review_(review_info)
        except:
            pass
        
        # Create df for every product:
        df = pd.DataFrame(review_info)
        df['total_review'] = total_review
        df['Date'] = dat
        df['Time'] =  cur_time
        df['Product_platform'] = i[1]
        df['Product_Category'] = i[2]
        df['Product_id'] =  i[3]
        df['Product_Urls'] = i[4]
        df['Product_name'] = product_name
        
        df2.to_sql('Sentimark_review', con=engine, if_exists='append', index=False)
                       
    driver.close()                   
    
    
    
