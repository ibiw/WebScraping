
class WebScraping():

    element = None

    def __init__(self):
        pass

    def __str__(self):
        return 'Web Scraping with Python'
        
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

        sum = len(stocks)
        count = 1
        while count <= sum:
            driver = webdriver.PhantomJS(service_args=['--webdriver-loglevel=ERROR'], service_log_path='/tmp/ghostdriver.log')
            for stock in stocks:

                # driver = webdriver.PhantomJS(service_args=['--webdriver-loglevel=ERROR'], service_log_path='/tmp/ghostdriver.log')
                # time.sleep(2)
                
                print('{}/{}'.format(count, sum))
                count += 1

                data = []
                stock = stock.replace(' ', '')
                url = 'https://finance.yahoo.com/quote/' + stock + '/key-statistics'
                print(url)

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
                    # pass
                    # driver.quit()
                    # quit PhantomJS and release all the resource after runnning 25 times
                    if count % 25 == 0:
                        print('------>{}'.format(count))
                        driver.quit() 
                        time.sleep(2)
                        driver = webdriver.PhantomJS(service_args=['--webdriver-loglevel=ERROR'], service_log_path='/tmp/ghostdriver.log')
                        time.sleep(1)

            # quit PhantomJS after for loops
            driver.quit()
            return keyStatList

    # get data with pd.read_html from ca.finance.yahoo.com
    @staticmethod
    def ksyStatCompetitiors(stocks):
        # from pandas_datareader import data
        import pandas as pd
        from time import sleep

        selects = []
        # all_a3 = ['AAON', 'AMBA', 'ATRI', 'BSTC', 'CPLA', 'CPSI', 'DHIL', 'DORM', 'ENTA', 'ENZN', 'FRAN', 'INSY', 'IQNT', 'IRMD', 'ITRN', 'VIVO', 'MNDO', 'OFLX', 'PETS', 'SLP', 'STRA', 'TSRA', 'UG', 'WETF', 'SAM', 'BPT', 'BKE', 'LXFT', 'MED', 'MTR', 'MSB', 'PZN', 'SBR', 'RGR', 'TNH', 'WHG']
        # stocks = ['FTNT']
        
        ## the works url now is: ca.finance.yahoo.com
        ## the url of Competitiors: url = https://ca.finance.yahoo.com/q/co?s=ENTA+Competitors

        for stock in stocks:
            # stock = stock.replace(' ', '')
            url = 'https://ca.finance.yahoo.com/q/co?s=' + stock + '+Competitors'
            print(url)
            df = pd.read_html(url)
            print(len(df))
            # print(df[4])
            if len(df) >= 5:	## avoid empty data, please note the value 4 and 5

                try:
                    df = df[4]	## choose the right list, and df is a dataframe
                    # print(len(df))
                    df.columns = df.iloc[1]	## replace the columns of numbers with strings
                    #print(df)
                    pe = df[[stock, 'Industry']].iat[11, 0]
                    pe_industry = df[[stock, 'Industry']].iat[11, 1]
                    print(pe, type(pe), pe_industry, type(pe_industry))
                    if isinstance(pe, float) or isinstance(pe_industry, float):
                        print('One or more P/E is N/A', stock)
                    elif isinstance(pe, str) and isinstance(pe_industry, str):
                        pe = float(pe)
                        pe_industry = float(pe_industry)
                        print(pe, type(pe), pe_industry, type(pe_industry))
                        if pe/pe_industry < 0.85:
                            selects.append(stock)
                            print('Founded, and P/E divided by P/E Industry is :', pe/pe_industry)
                        else:
                            print('\tPass')
                except KeyError as e:
                    print(e)
            else:
                print("Empty Data:\t", stock)
            sleep(0.01)
        print(selects)
        print('---All done!')
        return(selects)


# the url for Yahoo key statistic 
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

def main():
    # sfiles = ['nasdaq.csv', 'nyse.csv', 'amex.csv']
    # # sfiles = ['nyse.csv']
    # for file in sfiles:
    #     print('-'*20 + file + '-'*20)
        
    #     stocks = WebScraping.getSymbol(file)
    #     data = WebScraping.seleniumGet(stocks)
    #     print('The following symbols are from: {}\n'.format(file.split('.')[0]), data)

    # from keystat_0813 import stocks
    # print(stocks)
    # data = WebScraping.ksyStatCompetitiors(stocks)
    # print(data)

    stocks = []
    with open('tsx.txt') as f:
        for line in f:
            stocks.append(line.strip())
    # print(stocks)
    data = WebScraping.seleniumGet(stocks)
   



if __name__ == '__main__':
    main()