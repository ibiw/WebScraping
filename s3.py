from pandas_datareader import data
import pandas as pd
import datetime
import io, sys
import pickle
import numpy as np
from time import sleep

today = datetime.datetime.now().strftime("%Y, %m, %d")
stock_watch_list = ["^GSPC", "^IXIC", "^DJI","FTNT", "TWTR", "ECA", "CNQ.TO"]
currency_list = ["DEXCNUS", "DEXCAUS", "DEXCNCA", "DEXCACA", "DEXUSEU"]

start = datetime.datetime(2009, 11, 18)
end = datetime.datetime(2016, 4, 15)
#end = datetime.datetime(2013, 1, 27)
#help(data)
#help(wb)
# f=data.DataReader("FTNT", 'yahoo', start)
#print(f.resample('W').tail())

#print(f.ix['2016-03-24'])
#print(f)
#print(f)
#df = pd.concat([f], axis=0)
# df = f
# #print(df.head())

# df["Day_High_3"] = pd.Series.rolling(df.High, window=3, min_periods=1).max()
# df["Day_Low_3"] = pd.Series.rolling(df.Low, window=3, min_periods=1).min()
# df["MA_10"] = pd.Series.rolling(df.Close, window=10, center = False).mean()
# df["MA_20"] = pd.Series.rolling(df.Close, window=20, center = False).mean()


def _get_yahoo(stock, start):
	df = data.DataReader(stock, 'yahoo', start)
	return df

def _moving_average(df, x):			##  get the x days/weeks/months close price moving average 
	new_column = "MA_" + str(x)
	df[new_column] = pd.Series.rolling(df.Close, window = x, center = False).mean()

def _moving_average_up_cross(ma1, ma2):
	ma1 = _moving_average

def _periods_index(df):			## for _periods to adjust the date
	new_index = []				## the new index changes format '2016-02-29/2016-03-06' to '2016-02-29'
	for x in df.index:
		x = str(x).split('/')[0]
		new_index.append(x)
	df.index = new_index

def _periods(df, period):
	if period == 'W':
		df = df.to_period('W')
	elif period == 'M':
		df = df.to_period('M')
	else:
		exit("Please use 'W' for Weekly or 'M' for Monthly.")

			## row weekly data
	col_order = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']		## the columns order after aggregation
	agg_weekly = {'Open' : 'first',			## get the corresponding record from each row in the same week
				'High' : max,
				'Low' : min,
				'Close' : 'last',
				'Volume' : sum,
				'Adj Close' : 'last'}

	agg_data = df.groupby(df.index).agg(agg_weekly)[col_order]
	_periods_index(agg_data)
	return agg_data

def _daily_watch_stock(stock_watch_list):
	## get latest 5 days data first to avoid holidays and weekends
	today = datetime.datetime.now()
	date = today - datetime.timedelta(days = 5)	
	df = pd.DataFrame()

	for stock in stock_watch_list:
		stock_data = _get_yahoo(stock, date)

		df = df.append(stock_data.tail(1))		## choose the latest one
		#df = df.join(tmp)
	#df.index = stock_watch_list
	#df.reset_index(level = 0, inplace = True)	
	print(df.index[0])
	df.index = stock_watch_list
	print(df[['Open', 'Adj Close', 'High', 'Low', 'Volume']])
	print("\n^GSPC is S&P 500\t^IXIC is NASDAQ\t\t^DJI is Dow")
	print("\n\n")

def _get_currency():
	url_usd = "http://www.x-rates.com/table/?from=USD&amount=1"
	url_cny = "http://www.x-rates.com/table/?from=CNY&amount=1"
	usd = pd.read_html(url_usd)
	usd = pd.DataFrame(usd[0])

	cny = pd.read_html(url_cny)
	cny = pd.DataFrame(cny[0])

	usd.index = usd["US Dollar"]
	cny.index = cny["Chinese Yuan Renminbi"]
	
	print(usd.iloc[[0, 1, 4, 9], [0, 1, 2]])
	print("\n")
	print(cny.iloc[[0, 5], [0, 1, 2]])
	print("\n\n")

def _get_Yhaoo_key_to_csv(stock_symbol, file_path):
	url = "https://finance.yahoo.com/q/ks?s=" + stock_symbol + "Key+Statistics"
	df = pd.read_html(url)
	print(type(df))
	df.to_pickle(file_path + '\\' + stock_symbol + '.scv')

def _select_stocks_key_stat():	

	# df = pd.read_csv("nasdaq.csv")	## 1
	# df = pd.read_csv("nyse.csv")	## 2
	# df = pd.read_csv("amex.csv")	## 3
	# stocks = df.Symbol
	all_a1 = ['AAON', 'ABMD', 'AEIS', 'ALGN', 'AFOP', 'AMBA', 'ANIK', 'ATRI', 'BSTC', 'BSQR', 'CPLA', 'CBOE', 'JRJC', 'CPSI', 'CRWS', 'CTCM', 'DHIL', 'DRAD', 'DMLP', 'DORM', 'ENTA', 'EFOI', 'ENZN', 'EXPD', 'EXPO', 'FHCO', 'FRAN', 'HCSG', 'HTLD', 'INSY', 'IQNT', 'LINK', 'ISRG', 'IRMD', 'IRIX', 'ITRN', 'LANC', 'TREE', 'LTBR', 'LLTC', 'LRAD', 'LULU', 'MKTX', 'VIVO', 'MSTR', 'MDXG', 'MNDO', 'MSON', 'MNST', 'FIZZ', 'OFLX', 'OXBR', 'PETS', 'SEIC', 'SILC', 'SIMO', 'SLP', 'SWKS', 'SEDG', 'SPOK', 'SHOO', 'STRA', 'SNHY', 'TROW', 'TSRA', 'RMR', 'ULTA', 'UTHR', 'UG', 'UTMD', 'VDSI', 'WETF', 'ZAGG', 'ZLTQ', 'AHC', 'ATHM', 'SAM', 'BPT', 'BKE', 'CATO', 'CMG', 'CBK', 'DSW', 'FIT', 'GLOB', 'GMED', 'HGT', 'INFY', 'LXFT', 'MPX', 'MJN', 'MED', 'MTR', 'MSB', 'KORS', 'MBLY', 'MSI', 'PRLB', 'PZN', 'REX', 'RHI', 'SBR', 'RGR', 'TARO', 'TNH', 'THO', 'VTRB', 'WHG', 'WGO', 'WNS', 'WPT', 'CQH', 'MGH', 'STS']
	stocks = ['BCOM']
	# stocks = all_a1
	selects = []
	#a1 = ['CTCM', 'ENTA', 'EFOI', 'ITRN', 'SPOK', 'UTHR', 'ZLTQ', 'SAM', 'GLOB', 'LXFT', 'MED', 'KORS', 'RHI']

	for stock_symbol in stocks:
		stock_symbol = stock_symbol.replace(' ', '')
		url = 'https://finance.yahoo.com/q/ks?s=' + stock_symbol + '+Key+Statistics'
		#url = 'https://finance.yahoo.com/q/ks?s=FIT+Key+Statistics'
		print(url)
		#https://finance.yahoo.com/q/ks?s=JNPR+Key+Statistics
		df = pd.read_html(url)
		print(len(df))
		print(df)
		if len(df) >= 15:

			market_cap = df[1].iat[5, 1]		## this is class str
			trailling_PE = df[1].iat[7, 1]      ## this is class str
			return_on_equity_df = df[12]		## this is a dataframe
			banlance_shert_df = df[15]			## this is a dataframe too, and it is includes totaldebt_equity and current_ratio
			#banlance_shert_df = pd.to_numeric(banlance_shert_df, errors = 'coerec')

			# x = (return_on_equity_df.iat[2, 1])
			# print(x)
			# print(type(x))
			# print(np.isnan(x))
			# if x == np.nan:
			# 	print("nananana")
			# print(return_on_equity_df[1][2:3].isnull())

			#print(banlance_shert_df[1][5:7])

			# return_on_equity  = return_on_equity_df[1][2:3]
			# totaldebt_equity = banlance_shert_df[1][5:6]
			# current_ratio  = banlance_shert_df[1][6:7]
			return_on_assets = return_on_equity_df.iat[1, 1]
			return_on_equity  = return_on_equity_df.iat[2, 1]
			totaldebt_equity = banlance_shert_df.iat[5, 1]
			current_ratio  = banlance_shert_df.iat[6, 1]

			print(market_cap, type(market_cap), trailling_PE, type(trailling_PE))
			print(return_on_assets, type(return_on_assets), return_on_equity, type(return_on_equity), totaldebt_equity, type(totaldebt_equity), current_ratio, type(current_ratio))

			# print(type(totaldebt_equity))
			# print(isinstance(totaldebt_equity, np.float64))
			# print(isinstance(totaldebt_equity, str))

			if isinstance(market_cap, np.float) or isinstance(market_cap, float):
				print("None 1: market_cap is N/A", stock_symbol)
				continue
			elif 'B' in market_cap and float(market_cap.replace('B', '')) > 2.0:
				print("None 2: market_cap > 2B", stock_symbol)
				continue
			elif isinstance(return_on_assets, np.float64) or isinstance(return_on_assets, float):
				print("None 3: return_on_assets", stock_symbol)
				continue			
			elif isinstance(return_on_equity, np.float64) or isinstance(return_on_equity, float):
				# if np.isnan(return_on_equity) or np.isnan(current_ratio.item):
				print("None 4: return_on_equity", stock_symbol)
				continue
			elif isinstance(current_ratio, np.float64) or isinstance(current_ratio, float):
				print("None 5: current_ratio", stock_symbol)
				continue
			else:
				if isinstance(totaldebt_equity, np.float64) or isinstance(totaldebt_equity, float):
					totaldebt_equity = 0.0
				if isinstance(return_on_assets, str):
					return_on_assets = return_on_assets.replace('%', '').replace(',', '')
					return_on_assets = float(return_on_assets)
				if isinstance(return_on_equity, str):
					return_on_equity = return_on_equity.replace('%', '').replace(',', '')
					return_on_equity = float(return_on_equity)
				if isinstance(totaldebt_equity, str):
					#return_on_equity = return_on_equity.replace('%', '')
					totaldebt_equity = float(totaldebt_equity)
				if isinstance(current_ratio, str):
					#return_on_equity = return_on_equity.replace('%', '')
					current_ratio = float(current_ratio)
				else:
					pass
				# return_on_equity = return_on_equity[1].replace('%', '')
				# return_on_equity = float(return_on_equity)
				# current_ratio = float(current_ratio[1])
				
			# if np.nan(totaldebt_equity):
			# 	totaldebt_equity = 0.00
			# else:
			# 	#totaldebt_equity = float(totaldebt_equity[1])
			# 	pass
			print(market_cap, type(market_cap), trailling_PE, type(trailling_PE))
			print(return_on_assets, type(return_on_assets),return_on_equity, type(return_on_equity), totaldebt_equity, type(totaldebt_equity), current_ratio, type(current_ratio))
			if return_on_assets > 15 and return_on_equity > 15 and totaldebt_equity < 0.4 and current_ratio > 2:
				selects.append(stock_symbol)
				print("********** Founded!!! ***********")
			else:
				print("\tPass")
		else:
			print("The lenght is less than 15!!!")
		sleep(0.01)
	print(selects)
	return(selects)

def _select_stocks_competitiors():
	selects = []
	all_a3 = ['AAON', 'AMBA', 'ATRI', 'BSTC', 'CPLA', 'CPSI', 'DHIL', 'DORM', 'ENTA', 'ENZN', 'FRAN', 'INSY', 'IQNT', 'IRMD', 'ITRN', 'VIVO', 'MNDO', 'OFLX', 'PETS', 'SLP', 'STRA', 'TSRA', 'UG', 'WETF', 'SAM', 'BPT', 'BKE', 'LXFT', 'MED', 'MTR', 'MSB', 'PZN', 'SBR', 'RGR', 'TNH', 'WHG']
	stocks = ['FTNT']
	#stocks = all_a3
	## the url of Competitiors: url = https://finance.yahoo.com/q/co?s=ENTA+Competitors

	for stock_symbol in stocks:
		stock_symbol = stock_symbol.replace(' ', '')
		url = 'https://ca.finance.yahoo.com/q/co?s=' + stock_symbol + '+Competitors'
		#url = 'https://finance.yahoo.com/q/ks?s=FIT+Key+Statistics'
		print(url)
		#https://finance.yahoo.com/q/ks?s=JNPR+Key+Statistics
		df = pd.read_html(url)
		print(len(df))
		# print(df[4])
		if len(df) >= 5:	## avoid empty data, please note the value 4 and 5
			df = df[4]	## choose the right list, and df is a dataframe
			# print(len(df))
			df.columns = df.iloc[1]	## replace the columns of numbers with strings
			#print(df)
			pe = df[[stock_symbol, 'Industry']].iat[11, 0]
			pe_industry = df[[stock_symbol, 'Industry']].iat[11, 1]
			print(pe, type(pe), pe_industry, type(pe_industry))
			if isinstance(pe, float) or isinstance(pe_industry, float):
				print('One or more P/E is N/A', stock_symbol)
			elif isinstance(pe, str) and isinstance(pe_industry, str):
				pe = float(pe)
				pe_industry = float(pe_industry)
				print(pe, type(pe), pe_industry, type(pe_industry))
				if pe/pe_industry < 0.85:
					selects.append(stock_symbol)
					print('Founded, and P/E divided by P/E Industry is :', pe/pe_industry)
				else:
					print('\tPass')
		else:
			print("Empty Data:\t", stock_symbol)
		sleep(0.01)

	print(selects)
	return(selects)

#result = pd.concat([a, b])
#print(result)

# print(_periods(f, "W").tail())

#_periods(df, 'M')
#print(df.head(3))


#eca = data.DataReader("ECA", 'yahooDa')
#print(eca)
#print(df.ix['24/3/2016'])
#df1 = pd.DataFrame(df)
#print(df[df.MA_10.shift(1) < df.MA_20.shift(1) and df.MA_10 > df.MA_20].loc[:, 'Close'])
"""
gc12 = df[(df.MA_10 > df.MA_20) & (df.MA_10.shift(1) < df.MA_20.shift(1))]
#print(gc12.loc[:, 'Close'])
print(gc12.index)

len_index = len(gc12.index)
print(len_index)
for i in range(len_index):
	if i < len_index - 1:
		print(df.loc[gc12.index[i]:gc12.index[i + 1], 'Close'])
		print("-" * 20)
	else:
		print(df.loc[gc12.index[i]:, 'Close'])
"""

#print(df.loc[:, 'Low'])
#x = df1.rolling(center=False,window=20).mean()
#print(df.loc[gc12.index[1]:, 'Close'])

# x = pd.read_excel('hpi_4_12_2016.xls')
# print(x.ix[0:10, [1, 2, 3, 7, 8]])

# _daily_watch_stock(stock_watch_list)

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')   

# df = pd.read_html("http://www.x-rates.com/table/?from=USD&amount=1")
# print(df[0])

# _get_currency()

# usdcad = data.DataReader('DEXCHUS', 'fred')
# print(usdcad)

# this works
# s_p = data.DataReader('^GSPC','yahoo')  # S&P 500
# nasdaq = data.DataReader('^IXIC','yahoo')  # NASDAQ

# # this doesn't
# dow = data.DataReader('^DJI','yahoo')   # Dow

# print(dow)
# df = pd.read_csv("nasdaq.csv")
# stocks = df.Symbol

# df_sort = df.sort_values(by = "MarketCap")[["Symbol", "MarketCap"]]
# df_sort.index = df.index
# #print(df_sort[["Symbol", "MarketCap"]].head())
# #print(df_sort[1308:1368])
# df_2b = df_sort.loc[df_sort["MarketCap"].isin(["$2B"])]
# print(df_2b)

# df = pd.read_html("https://finance.yahoo.com/q/ks?s=JNPR+Key+Statistics")
# print(type(df[12]))
# return_on_equity  = df[12].loc[2]
# print(return_on_equity [0], return_on_equity [1])
# totaldebt_equity = df[15].loc[5]
# current_ratio  = df[15].loc[6]

# print(totaldebt_equity[0], totaldebt_equity[1])
# print(current_ratio[0], current_ratio[1])
# nasdaq
# ['AAON', 'ABMD', 'AEIS', 'ALGN', 'AFOP', 'AMBA', 'ANIK', 'ATRI', 'BSTC', 'BSQR', 'CPLA', 'CBOE', 'JRJC', 'CPSI', 'CRWS', 'CTCM', 'DHIL', 'DRAD', 'DMLP', 'DORM', 'ENTA', 'EFOI', 'ENZN', 'EXPD', 'EXPO', 'FHCO', 'FRAN', 'HCSG', 'HTLD', 'INSY', 'IQNT', 'LINK', 'ISRG', 'IRMD', 'IRIX', 'ITRN', 'LANC', 'TREE', 'LTBR', 'LLTC', 'LRAD', 'LULU', 'MKTX', 'VIVO', 'MSTR', 'MDXG', 'MNDO', 'MSON', 'MNST', 'FIZZ', 'OFLX', 'OXBR', 'PETS', 'SEIC', 'SILC', 'SIMO', 'SLP', 'SWKS', 'SEDG', 'SPOK', 'SHOO', 'STRA', 'SNHY', 'TROW', 'TSRA', 'RMR', 'ULTA', 'UTHR', 'UG', 'UTMD', 'VDSI', 'WETF', 'ZAGG', 'ZLTQ']
# nyse
# ['AHC', 'ATHM', 'SAM', 'BPT', 'BKE', 'CATO', 'CMG', 'CBK', 'DSW', 'FIT', 'GLOB', 'GMED', 'HGT', 'INFY', 'LXFT', 'MPX', 'MJN', 'MED', 'MTR', 'MSB', 'KORS', 'MBLY', 'MSI', 'PRLB', 'PZN', 'REX', 'RHI', 'SBR', 'RGR', 'TARO', 'TNH', 'THO', 'VTRB', 'WHG', 'WGO', 'WNS', 'WPT']
# amex
# ['CQH', 'MGH', 'STS']

# _select_stocks_key_stat()
_select_stocks_competitiors()

#print(df.sort_values(by = "MarketCap")[["Symbol", "MarketCap"]].head(10))
# print(df.loc[]
