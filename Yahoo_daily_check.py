import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import sys
import re
#import json

pd.set_option('expand_frame_repr', False)

class daily_check():

	def __init__(self, url_login, username, passwd, headers, url_protfolio):
		self.url_login = url_login
		self.username = username
		self.passwd = passwd
		# self.urls = urls
		self.headers = headers
		self.url_protfolio = url_protfolio
		self.s = None
		self.my_protfolio_urls = []
		self.my_protfolio_names = []
	
	@staticmethod
	def ZacksRank(symbols):
		zacks_url_base = 'https://www.zacks.com/stock/quote/'
		
		with requests.Session() as s:
			ranks = []
			for symbol in symbols:
				url = zacks_url_base + symbol
				resp_data = s.get(url)
				resp_text = resp_data.text
				soup = BeautifulSoup(resp_text, 'lxml')
				rank_box = soup.find_all('div', {'class' : 'zr_rankbox'})
				## return None if there is no ranking
				def get_rank(rank_box):
					for item in rank_box:
						if '-' in item.text:
							return item.text.strip().split('-')[0]
				ranks.append(get_rank(rank_box))
						# return item.text.strip()
		return ranks


	def login(self):
		#details_1 = {'username': self.username, 'signin' : 'authtype', 'countrycode' : '1', 'seqid' : '2', '_format' : 'json'}
		#details_2 = {'username': self.username, 'passwd': self.passwd, 'countrycode' : '1', '_crumb' : 'fMM7l5K7yLa', '_ts' : '1462233682', '_format' : 'json'}
		details_2 = {'username': self.username, 'passwd': self.passwd, 'countrycode' : '1', '_crumb' : '1ISWfgxMS0Q', '_ts' : '1462247438', '_format' : 'json'}
		#details_2 = {'username': self.username, 'passwd': self.passwd}
		#details_2 = json.dumps(details_2)
		#print(data)
		#print(details_2)

		## if ranking is True, then display Zacks Ranking
		ranking = False
		choice = input('Display Zacks Ranking? Yes/No(No):')
		if 'y' in choice.lower():
			ranking = True
		with requests.Session() as self.s:
			#resp = self.s.post(url = self.url_login, data = details_1, headers = self.headers)
			resp = self.s.post(url = self.url_login, data = details_2, headers = self.headers)
			
			# get protfolios urls
			resp_data = self.s.get(self.url_protfolio)
			resp_text = resp_data.text.encode('utf-8').decode('ascii', 'ignore')
			soup = BeautifulSoup(resp_text, 'lxml')
			for a in soup.find_all('a', href=True):
				if re.findall('http://finance.yahoo.com/portfolio/', a['href']):
					self.my_protfolio_urls.append(a['href'])
					# self.my_protfolio_names.append(a.text)
			# change a list to set to remove duplicated items, the sort it. After sort, it changs to list again.
			# print(self.my_protfolio_urls)
			self.my_protfolio_urls = sorted(set(self.my_protfolio_urls))
			# self.my_protfolio_urls = list(set(self.my_protfolio_urls))
			# self.my_protfolio_names = set(self.my_protfolio_names)

			# for link in self.my_protfolio_urls:
			# 	print(link)

			for url in self.my_protfolio_urls:
				if 'p_16/view/v1' in url:
					continue
				try:
					print('\n\t', url)
					resp_data = self.s.get(url = url)
					resp_text = resp_data.text.encode('utf-8').decode('ascii', 'ignore')
					#resp_data.encoding = 'UTF-8'
					soup = BeautifulSoup(resp_text, 'lxml')
					#soup = soup.decode('utf-8', 'ignore')
					#print(resp.json())
					# resp_c1 = self.s.get(url = self.url_c1)
					# print(resp_c1.text)
					#print(resp.text)
					#print(resp_data.content)
					
					if "Yahoo - login" in resp_data.text:
						print("The email and password you entered don't match.")
					elif "CS1" in resp_data.text:
						print('-' * 76)
						table = soup.find('table', {'class' : 'yfi_portfolios_multiquote sortable yfi_table_row_order'})
						# df = pd.read_html(table)
						table_body = table.find('tbody')
						#df_index = range(45)
						df_columns = ['SYMBOL', 'NAME', 'TIME', 'PRICE', 'CHG', '% CHG', 'VOLUME', 'AVG VOL', 'D LOW', 'D HIGH', '50-DAY MA', '%50MA', 'MKT CAP', 'P\/E', 'P\/E NEXT YR', 'DIV PAY DATE', 'YIELD', 'MORE INFO']
						#df = pd.DataFrame(index = df_index, columns = df_columns)
						#print(df)
						pd_list = []
						for tr in table_body.find_all('tr'):
							td_list = []
							for td in tr.find_all('td'):
								if 'Chart' in td.text:
									continue
								else:
									#sys.stdout.write(td.text + '\t')
									td_text = td.text.replace(',', '').replace('%', '')
									# if td.text == '-':
									# 	td.text = np.nan
									td_list.append(td_text)
							#td_series = pd.Series(td_list)
							# print(td_list)
							pd_list.append(td_list)
							#df = df.append(td_series, ignore_index = True)
							#sys.stdout.write('\n')
						df = pd.DataFrame(pd_list, columns = df_columns)
						df.index = df.SYMBOL
						## change all coloumns to numeric if possible
						df = df.apply(lambda x: pd.to_numeric(x, errors='ignore'))
						# def color_negative_red(val):
						# 	"""
						# 	Takes a scalar and returns a string with
						# 	the css property `'color: red'` for negative
						# 	strings, black otherwise.
						# 	"""
						# 	color = 'red' if val < 0 else 'black'
						# 	return 'color: %s' % color
						
						# df = df.style.applymap(color_negative_red)
						# ranks = []
						# for item in df.index:
						# 	ranks.append(self.ZacksRank(item))
						# print(ranks)
						# df['R'] = ranks
						# df['VOL%'] = df['VOLUME'] / df['AVG VOL']


						#print(df.sort_values(by = '% CHG')[['% CHG', 'PRICE', 'DAY\'S LOW', 'DAY\'S HIGH', 'VOLUME', 'AVG VOL']])
						if '/p_1/view/v3' not in url:
							df['VOL %'] = df['VOLUME'] / df['AVG VOL']
							if ranking:
								ranks = self.ZacksRank(df.index)
								df['R'] = ranks
								print(df[['% CHG', 'PRICE', 'D LOW', 'D HIGH', 'VOL %', '%50MA', 'R']])
							else:
								print(df[['% CHG', 'PRICE', 'D LOW', 'D HIGH', 'VOL %', '%50MA']])
						else:
							print(df[['% CHG', 'PRICE', 'D LOW', 'D HIGH', 'VOLUME']])							
						#print(df.columns)
					else:
						print("Nothing")
				except AttributeError as e:
					print(e)

def main():
	username = "ibiw@yahoo.cn"
	passwd = "ThePassw0rdHa$h" ##ThePassw0rdHa$h
	signin = ""
	#url_login = "https://login.yahoo.com/config/login?.src=quote&.intl=us&.lang=en-US&.done=https://finance.yahoo.com/"
	url_login = 'https://login.yahoo.com/config/login'
	url_protfolio = 'https://finance.yahoo.com/portfolio/p_11/view?bypass=true'
	# urls = ['https://finance.yahoo.com/portfolio/pf_1/view/v3', 'https://finance.yahoo.com/portfolio/p_6/view/v3', 'https://finance.yahoo.com/portfolio/p_1/view/v3', 'https://finance.yahoo.com/portfolio/p_7/view/v3']
	headers = {'Host': 'login.yahoo.com',
			'Connection': 'keep-alive',
			#'Origin': 'https://digitalvita.pitt.edu',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
			'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'X-Requested-With' : 'XMLHttpRequest', 
			'Referer': 'https://login.yahoo.com/config/login',
			#'Content-Length' : '182',
			'Cookie': 'B=c81d651big80e&b=3&s=se',
			'Accept-Encoding': 'gzip, deflate, br',
			'Content-Length': '167',
			# 'DTN' : " 1",
			'Accept-Language': 'en-US,en;q=0.5'	}


	dc = daily_check(url_login, username, passwd, headers, url_protfolio)
	dc.login()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit('\nExit through KeyboardInterrupt, Bye-Bye.')