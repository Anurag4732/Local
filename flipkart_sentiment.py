i = 'https://www.flipkart.com/samsung-series-4-80cm-32-inch-hd-ready-led-smart-tv/p/itmf5xzyyfcfcjdn?pid=TVSF5XZYHQRPXVJ6&fm=SEARCH&ppt=dynamic&ppn=dynamic&ssid=flp05gakn40000001596630476825'
U = 'p/'
R = i.split(U)
L = str(R[0]) + 'product-reviews/' + str(R[1])
driver.get(L)

from time import sleep
from selenium import webdriver
import pandas as pd
import numpy as np
import re
import time
import calendar

review_info = {
                'rating':[],
                'title':[],
                'sentiment_date':[],
                'review':[],
                'like':[],
                'dislike':[]
                }

def review_(review_info):
    ## It's review and rating session that's we used len(rating) 
    try:
        number_rating_review = len(driver.find_elements_by_css_selector("div[class^=hGSR34 ]"))
        if number_rating_review > 1:  ## there are 10 customers rating and one overall rating
            for i in range(1, number_rating_review): 
                try:
                    review_info['rating'].append(int(driver.find_elements_by_css_selector("div[class^=hGSR34 ]")[i].text))
                except:
                    review_info['rating'].append(0)
                try: # Other review information are 10 only 
                    review_info['title'].append(driver.find_elements_by_xpath("//p[@class = '_2xg6Ul']")[i-1].text)
                except:
                    review_info['title'].append('Not Available')
                try:
                    present = 8  ## Present month august = 8
                    pr_year = ', 2020'
                    if 'ago' in driver.find_elements_by_xpath("//p[@class = '_3LYOAd']")[i-1].text:
                        pr_month = driver.find_elements_by_xpath("//p[@class = '_3LYOAd']")[i-1].text
                        pr_month = present - int(pr_month.split('month')[0])  ## 10months ago
                        if pr_month == 0:
                            pr_month = 'January'
                        else:
                            pr_month = calendar.month_name[pr_month]
                        review_info['sentiment_date'].append(pr_month + pr_year)
                    else:
                        review_info['sentiment_date'].append(driver.find_elements_by_xpath("//p[@class = '_3LYOAd']")[i-1].text)
                except:
                    review_info['sentiment_date'].append('Not Available')

                try: ## If there is:- 'Read More'
                    if driver.find_element_by_xpath("//span[@class = '_1EPkIx']").is_displayed():
                        driver.find_element_by_xpath("//span[@class = '_1EPkIx']").click() 
                        time.sleep(0.5)
                        review_info['review'].append(driver.find_elements_by_xpath("//div[@class = 'qwjRop']")[i-1].text)

                except:
                    try:
                        review_info['review'].append(driver.find_elements_by_xpath("//div[@class = 'qwjRop']")[i-1].text)
                    except:
                        review_info['review'].append('Not Available')

                try:
                    review_info['like'].append(int(driver.find_elements_by_xpath("//div[@class = '_2ZibVB']")[i-1].text))
                except:
                    review_info['like'].append(0)
                try:
                    review_info['dislike'].append(int(driver.find_elements_by_xpath("//div[@class = '_2ZibVB _1FP7V7']")[i-1].text))
                except:
                    review_info['dislike'].append(0)
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
    ## For this type only:- 363 Ratings & 48 Reviews
    total_review = int(driver.find_element_by_xpath("//span[@class = '_38sUEc']").text.split('&')[1].split()[0])
except:
    total_review = 0

review_info = review_(review_info) # If there is no review, at that time it will also run for one time
## Loop for every page.........At here
df = pd.DataFrame(review_info)
df['total_review'] = total_review
df
