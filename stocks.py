#!/usr/bin/python

from yahoo_finance import Share
from yahoo_finance import Currency
import sys

#Stock_List = ["ECA", "CNQ", "CNQ.TO", "TWTR", "CTBK", "FTNT", "ANET"]
Stock_List = ["ECA", "CNQ.TO", "TWTR", "FTNT", "ANET", "BABA", "CNQ"]
Currency_List = ["USDCAD", "USDCNY", "CADCNY", "EURCNY", "EURUSD"]

## bold message
## http://www.darkcoding.net/software/pretty-command-line-console-output-on-unix-in-python-and-go-lang/
def bold(msg):
  return u'\033[1m%s\033[0m' % msg

## color message
## This is color 31 is Red
## This is color 32 is Green
## def color(this_color, string):
##  return "\033[" + this_color + "m" + string + "\033[0m"
def color(xyz):
  if '-' in xyz:
    return "\033[" + '31' + "m" + str(xyz) + "\033[0m"
  else:
    return "\033[" + '32' + "m" + str(xyz) + "\033[0m"
## def print_bold(xyz):
##  class style:
##    BOLD = '\033[1m'
##    END = '\033[0m'
##  print style.BOLD + xyz + style.END

## print column items for stock
def print_stock_columns():
  print bold("Stock\tPrice\tOpen\tChange\tDays_H\tDays_L\tYear_H\tYear_L")
  print "+"*62
## print column items for currency
def print_currency_columns():
  print bold("Currency\tRate")  
  print "+"*22

def get_currency(exchange):
  currency = Currency(exchange)
  rate = currency.get_rate()
  print exchange +"\t\t", str(rate)
  print "-"*22

def get_stock(stock_symbol):
  yahoo = Share(stock_symbol)
  price = yahoo.get_price()
  open = yahoo.get_open()
  days_high = yahoo.get_days_high()
  days_low = yahoo.get_days_low()
  year_high = yahoo.get_year_high()
  year_low = yahoo.get_year_low()
  change = yahoo.get_change()
  #change = str(yahoo.get_change())
  print stock_symbol + "\t", price + "\t", open + "\t", color(change) + "\t", days_high + "\t", days_low + "\t", year_high + "\t", year_low + "\t"
  #print bold(symbol)
  #print  "\t", (price) + "\t", open + "\t", change + "\t", days_high + "\t", days_low + "\t", year_high + "\t", year_low + "\t"
  print "-"*62
  return

#print bold("Stock\tPrice\tOpen\tChange\tDays_H\tDays_L\tYear_H\tYear_L")
#print "+"*62
file = "/var/www/stock.log"
html_file = "/var/www/stock.html"

def txt_to_html(txt, html):
  contents = open(txt,"r")
  with open(html, "w") as e:
    for lines in contents.readlines():
      e.write("<pre>" + lines + "</pre> <br>\n")

##### start
#####xxxxxxxxxxxxxxx
##### pint into file
#print 'Dive in'
#saveout = sys.stdout
#fsock = open(file, 'w')
#sys.stdout = fsock

print_currency_columns()
for currency in Currency_List:
  get_currency(currency)

print "\n"

print_stock_columns()
for symbol in Stock_List:
  get_stock(symbol)

##### print into fie
#sys.stdout = saveout
#fsock.close()
#txt_to_html(file, html_file)
