def Flipkart_scrap(engine):
    from datetime import datetime
    query = """
    select Platform,Category,id,Url from url_read_sample where Platform = 'Flipkart'
    """
    dfs = pd.read_sql_query(query, engine)

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//div[@class = '_1S11PY']").is_displayed():
                return("Low Stock Available")
        except:
            pass
        try:
            if driver.find_element_by_xpath("//div[@class = '_1mzTZn']").is_displayed():
                return("Stock Not Available")
        except:
            pass

        try:
            if driver.find_element_by_xpath("//div[@class = '_9-sL7L']").is_displayed():
                return("Stock Not Available")
        except:
            pass
        try:
            if driver.find_element_by_xpath("//span[@class='_35KyD6']").is_displayed():
                return("Stock Available")
        except:
            return("Stock Not Available")
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/qdgrees/Downloads/chromedriver')
    
    for i in dfs.itertuples():
        driver.get(i[4])
        time.sleep(2)
        pin_code = pin_
        driver.find_element_by_xpath("//input[@class = '_3X4tVa']").send_keys(pin_code)
        driver.find_element_by_xpath("//input[@class = '_3X4tVa']").send_keys(6*Keys.BACKSPACE)
        driver.find_element_by_xpath("//input[@class = '_3X4tVa']").send_keys(Keys.ENTER)
        time.sleep(2)
        break

    for i in dfs.itertuples():
        Product_MRP = []
        Product_Selling_Price = []
        Product_discount = []
        Seller = []

        driver.get(i[4])
        pid = i[4].split('?pid=')[1].split('&')[0]
        sleep(2)
        stock = out_of_stock()
        try:
            try:
                product_name = driver.find_element_by_xpath(
                    "//span[@class='_35KyD6']").text
            except:
                product_name = "Not Available"
            if driver.find_element_by_xpath("//span[@class='_37fzmc']").is_displayed():

                s_page = driver.find_element_by_xpath(
                    "//span[@class='_37fzmc']").click()
                sleep(2)

                # try:
                #     product_name = driver.find_element_by_xpath(
                #         "//div[@class='Sw6kZ2']/span").text
                # except:
                #     product_name = "Not Available"

                seller_names = driver.find_elements_by_xpath(
                    "//div[@class='_3fm_R4']/span")
                for name in seller_names:
                    Seller.append(name.text)
                try:
                    Disc_Prices = driver.find_elements_by_xpath(
                        "//div[@class = '_1vC4OE']")
                    for Disc_Price in Disc_Prices:
                        Disc_Price = float(re.sub('[₹,]', "", Disc_Price.text))
                        Product_Selling_Price.append(Disc_Price)
                except:
                    Product_Selling_Price.append("Not Available")

                try:
                    MRPs = driver.find_elements_by_xpath(
                        "//div[@class = '_3auQ3N']")
                    for MRP in MRPs:
                        MRP = float(re.sub('[₹,]', "", MRP.text))
                        Product_MRP.append(MRP)
                except:
                    Product_MRP.append("Not Available")

                try:
                    Discounts = driver.find_elements_by_xpath(
                        "//div[@class = 'VGWI6T']/span")
                    for Discount in Discounts:
                        discount = Discount.text.split(' off')[0]
                        Product_discount.append(discount)
                except:
                    Product_discount.append("Not Available")

                df = pd.DataFrame({'Product_MRP': pd.Series(Product_MRP),
                                   'Product_Selling_Price': pd.Series(Product_Selling_Price),
                                   'Product_discount': pd.Series(Product_discount), 'Seller': pd.Series(Seller)})
                df['Product_name'] = product_name
                df['Date'] = dat
                df['Time'] = cur_time
                df['Product_Category'] = i[2]
                df['Product_platform'] = i[1]
                df['Product_availability'] = stock
                df['Product_id'] = i[3]
                df['Product_Urls'] = i[4]
                df['asin_code'] = pid
                df['pin_code'] = pin_
                
                df = df[['Date', 'Time', 'Product_Category', 'Product_platform',
                         'Product_name', 'Product_id',
                         'Product_MRP', 'Product_Selling_Price','pin_code',
                         'Product_discount', 'Seller', 'Product_availability', 'Product_Urls', 'asin_code']]
                df.to_sql('scrapped_data_8', con=engine,
                          if_exists='append', index=False)

        except:
            try:
                product_name = driver.find_element_by_xpath(
                    "//span[@class='_35KyD6']").text
            except:
                product_name = "Not Available"

            try:
                Discounted_Price = driver.find_element_by_xpath(
                    "//div[@class = '_1vC4OE _3qQ9m1']").text
                Discounted_Price = float(re.sub('[₹,]', "", Discounted_Price))
            except:
                Discounted_Price = "Not Available"

            try:
                Price = driver.find_element_by_xpath(
                    "//div[@class = '_3auQ3N _1POkHg']").text
                Price = float(re.sub('[₹,]', "", Price))
            except:
                Price = "Not Available"
            try:
                discount = round(((Price - Discounted_Price) / Price) * 100)
                discount = (str(discount) + "%")
            except:
                discount = (str(0) + "%")
            try:
                Seller_1 = driver.find_element_by_xpath(
                    "//div[@class='_3HGjxn']/span/span").text
            except:
                Seller_1 = "Not Available"

            df = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2],
                               'Product_platform': i[1], 'Product_name': product_name,
                               'Product_id': i[3], 'Product_MRP': Price,
                               'Product_Selling_Price': Discounted_Price,
                               'Product_discount': discount, 'Seller': Seller_1,'pin_code':pin_
                               'Product_availability': stock, 'Product_Urls': i[4], 'asin_code': pid}, index=[0])
            df.to_sql('scrapped_data_8', con=engine,
                      if_exists='append', index=False)

    driver.close()
    
for pin_ in [700001, 400052, 560034, 110052, 500001]:
    Flipkart_scrap(engine, pin_)
