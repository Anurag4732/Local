def vasanth_and_co(engine):
    query = """
    select Platform,Category,id,Url from url where Platform = 'Vasanth and Co'
    """
    dfs = pd.read_sql_query(query, engine)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/home/saurabhtiwari/Downloads/chromedriver_linux64/chromedriver')

    def out_of_stock():
        try:
            if driver.find_element_by_xpath("//div[@class = 'title-product']").is_displayed:
                try:
                    if driver.find_element_by_xpath("//div[@class='stock']").text == 'Availability: Out Of Stock':
                        return("No Stock Available")  
                    else:
                        return("Stock Available")
                except:
                    return("Stock Available")
        except:
            return('Not Available')

    for i in dfs.itertuples():
        driver.get(i[4])
        sleep(3)
        try:
            product_name = driver.find_element_by_xpath("//div[@class = 'title-product']").text
        except:
            product_name = "Not Available"

        try:
            Discounted_Price = float(re.sub('[₹,]','',driver.find_element_by_xpath("//div[@class='product_page_price price']//span[@class = 'price-new']").text))
        except:
            Discounted_Price = "Not Available"

        stock = out_of_stock()

        try:
            driver.find_element_by_xpath("//input[@class = 'autosearch-input form-control']").send_keys(product_name)
            driver.find_element_by_xpath('//button[@class="button-search btn btn-default btn-lg"]').click()
            time.sleep(3)
            if driver.find_element_by_xpath('//h4//a').text.lower() == product_name.lower(): # In case there is not same product
                try:
                    Price = float(re.sub('[₹,]', '',driver.find_element_by_xpath("//span[@class = 'price-old']").text))  # mrp  
                except:
                    Price = "Not Available"
        except:
            Price = "Not Available"

        try:
            discount = round(((Price - Discounted_Price) / Price) * 100)
            discount = (str(discount) + "%")
        except:
            discount = (str(0) + "%")

            
        df2 = pd.DataFrame({'Date': dat, 'Time': cur_time, 'Product_Category': i[2], 'Product_platform': i[1], 'Product_name': product_name, 'Product_id': i[3], 'Product_MRP': Price,
                            'Product_Selling_Price': Discounted_Price, 'Product_discount': discount, 'Seller': i[1], 'Product_availability': stock, 'Product_Urls': i[4]}, index=[0])
        df2.to_sql('Scrapped_data_1', con=engine,
                   if_exists='append', index=False)
    driver.close()
