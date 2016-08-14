
class WebScraping():

    element = None

    def __init__(self):
        pass

    def __str__():
        return 'Web Scraping with Python'
        
    # @classmethod
    # def pd(cls, url):
    #     import pandas as pd
    #     df = pd.read_html(url)
    #     return df

    # @classmethod
    # def requests_get(cls, url):
    #     import requests
    #     from bs4 import BeautifulSoup
       
    #     # headers = {
    #     #     'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     #     'Accept-Encoding' : 'gzip, deflate, br',
    #     #     'Accept-Language' : 'en-US,en;q=0.5',
    #     #     'Cache-Control' : 'max-age=0',
    #     #     'Connection' : 'keep-alive',
    #     #     'Cookie ' : 'B=1lu3d6tbqko71&b=3&s=j9; PRF=t%3DFTNT; DNT=1',
    #     #     'DNT' : '1', 
    #     #     'Host' : 'finance.yahoo.com', 
    #     #     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}       

    #     with requests.Session() as s:
    #         resp = s.get(url = url, headers = headers)
    #         # resp.json()
    #         resp_text = resp.text.encode('utf-8').decode('ascii', 'ignore')
    #         soup = BeautifulSoup(resp_text, 'lxml')

    #         # d2 = soup.find('div', class_ = 'W(100%) Pos(r)')

    #         d2 = soup.find_all('data-reactid')

    #         print(type(soup))
    #         print(type(d2))
    #         # print(d2)
    #         # tables = d2.find_all('table')
    #         # print(len(tables))
    #         return(d2)

    @classmethod
    def getSymbol(cls, csvFile):
        import pandas as pd
        df = pd.read_csv(csvFile)
        stocks = df.Symbol
        return stocks

    @classmethod
    def yahooKeyStat(cls, roa, roe, de_ratio, current_ratio):
        
        print(type(roa), type(roe), type(de_ratio), type(current_ratio))
        # ecliusive roa, roe, and current_ratio with 'N/A' and negetive valuse, and format them
        if roa != 'N/A' and roe != 'N/A' and current_ratio != 'N/A' and '-' not in roa and '-' not in roe:
        # if (roa or roe or current_ratio) != 'N/A' and '-' not in (roa and roe):
            roa = float(roa.replace('%', '').replace(',', ''))
            roe = float(roe.replace('%', '').replace(',', ''))

            if de_ratio == 'N/A':
                de_ratio = 0
            else:
                de_ratio = float(de_ratio.replace(',', ''))
            roa, roe, current_ratio = float(roa), float(roe), float(current_ratio.replace(',', ''))

            if (roa > 15) and (roe > 15) and (de_ratio < 0.4) and (current_ratio > 2):
                print('---> Founded!')
                return True
       
        else:
            # print(cls, roa, roe, de_ratio, current_ratio)
            print('Hurry on!')
            return False

    
    @classmethod
    def seleniumGet(cls, stocks):
        from selenium import webdriver
        from selenium.common.exceptions import NoSuchElementException, TimeoutException
        import time
        import sys

        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        keyStatList = []

        # driver = webdriver.Firefox()
        # driver = webdriver.Chrome()
        # driver = webdriver.PhantomJS(service_args=['--webdriver-loglevel=ERROR'], service_log_path='/tmp/ghostdriver.log')
        # driver = webdriver.PhantomJS()
        # driver.get(url)
        # time.sleep(5)
        sum = len(stocks)
        count = 1

        for stock in stocks:
            driver = webdriver.PhantomJS(service_args=['--webdriver-loglevel=ERROR'], service_log_path='/tmp/ghostdriver.log')
            # time.sleep(2)
            
            print('{}/{}'.format(count, sum))
            count += 1

            data = []
            stock = stock.replace(' ', '')
            url = 'https://finance.yahoo.com/quote/' + stock + '/key-statistics'
            print(url)
            # TimeoutError urllib.error.URLError
            try:
                driver.get(url)
                # time.sleep(1.5)
                try:
                        t = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//head/title[contains(., 'Yahoo Finance')]")))

                        if 'Yahoo Finance' in driver.title:
                            print(driver.title) 
                            # roa = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@data-reactid, '$RETURN_ON_ASSETS')]")))
                            roa = driver.find_element_by_xpath("//*[contains(@data-reactid, '$RETURN_ON_ASSETS')]").text.rsplit(' ', 1)[1]
                            roe = driver.find_element_by_xpath("//*[contains(@data-reactid, '$RETURN_ON_EQUITY')]").text.rsplit(' ', 1)[1]
                            de_ratio = driver.find_element_by_xpath("//*[contains(@data-reactid, '$TOTAL_DEBT_TO_EQUITY')]").text.rsplit(' ', 1)[1]
                            current_ratio = driver.find_element_by_xpath("//*[contains(@data-reactid, '$CURRENT_RATIO')]").text.rsplit(' ', 1)[1]

                            # xpath how to:
                            # //td[text()="${nbsp}"]
                            # //table[@id='TableID']//td[text()=' '] ?
                            # //readAudit[@id='root'][1]
                            # //a[contains(@prop,'Foo')]

                            # split last character with rsplit
                            data.extend([roa, roe, de_ratio, current_ratio])
                            print(data)

                            if WebScraping.yahooKeyStat(data[0], data[1], data[2], data[3]):
                                keyStatList.append(stock)
                                print(keyStatList)

                except NoSuchElementException:
                    print('NoSuchElementException')
                
                except TimeoutException:
                    print('TimeoutException')

                # else:
                #     print('Unexcepted Error')

                finally:
                    pass

            finally:
                driver.quit()

        return(keyStatList)

# ftnt = 'https://finance.yahoo.com/quote/FTNT/key-statistics'

def test():
    stocks = ['ftnt', 'fit', 'anet']
    for stock in stocks:
        print(stock)
    WebScraping.seleniumGet(stocks)
# print(WebScraping.seleniumGet('fit'))

      # df = pd.read_csv("nasdaq.csv")	## 1
        # df = pd.read_csv("nyse.csv")	## 2
        # df = pd.read_csv("amex.csv")	## 3

# sfiles = ['nasdaq.csv', 'nyse.csv', 'amex.csv']
sfiles = ['nyse.csv']
for file in sfiles:
    stocks = WebScraping.getSymbol(file)
    data = WebScraping.seleniumGet(stocks)
    print(data)


