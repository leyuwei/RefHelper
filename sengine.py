# -*- coding:utf-8 -*-

import requests
import urllib.parse
import urllib
import urllib3
import time
import re
import random
import json
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar

class sengine:

	# 版本 1.0 Build20180927
	# 作者 GitHub / leyuwei  @ SEU
	# 使用Google Scholar / Baidu Xueshu引擎自动完成参考文献格式化，使用时可能需要挂载VPN
	# 使用时请保证输入 (1)文献名之间没有下划线 ; (2)可以包含作者，作者与文献名之间需用下划线分割但前后顺序可任意 ;
	#                  (3)可以有文献标号，格式为[1]中括号 ; (4) 最好不要包括在线网址、在线文章等引用，这些部分需要自行添加

	"""
	版本更新日志
	V 1.0
	-----------
	- 新增Google学术搜索引擎，支持批量参考文献清洗和标准BIBTEX格式导出
	- 新增Baidu学术搜索引擎，支持批量参考文献清洗和标准BIBTEX格式导出
	- 新增反扒机制对抗措施，对高频次访问情形进行随机延迟，并加入请求头Referer循环依赖设计
	"""

	__wrong_reflist = []
	__session = ''
	__proxies = ''
	__engine = ''
	__last_params = ''
	__last_keyword = ''
	__need_str = False
	__url_gscholar = 'https://scholar.google.com/scholar'
	__header_gscholar = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
		'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://scholar.google.com/scholar'}
	__url_bdscholar = 'http://xueshu.baidu.com/s'
	__url_bdscholar_cite = 'http://xueshu.baidu.com/u/citation'
	__header_bdscholar = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
		'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Referer': 'http://xueshu.baidu.com/s',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
		'Host': 'xueshu.baidu.com'}

	def __init__(self, proxies='127.0.0.1:1080', engine='google', need_str=False):
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁用安全警告
		self.__session = requests.Session()
		self.__session.cookies = CookieJar()
		self.__proxies = proxies
		self.__engine = engine
		self.__need_str = need_str

	def do_search_g(self, kw):
		# 单条文献检索并格式化为BIBTEX格式 使用Google引擎
		# Stage 1 - search for the corresponding article
		kw = self.__clean_reflist(kw)   # 对输入文献串进行清洗
		params_1 = self.__encode_params(kw, param_opt=0)
		header = self.__header_gscholar
		url = self.__url_gscholar
		last_url = url + '?' + urllib.parse.urlencode(self.__last_params)
		header['Referer'] = last_url
		self.__last_params = params_1
		r = self.__request_data(params_1, url, header)
		if r.find('gs_r gs_or gs_scl') >= 0:
			bs = BeautifulSoup(r, 'html.parser')
			cid = bs.findAll('div', {'class': 'gs_r gs_or gs_scl'})[0].attrs['data-cid']
			# Stage 2 - get bib
			params_2 = self.__encode_params(kw, param_opt=1, cid=cid)
			r = self.__request_data(params_2, url, header)
			bs = BeautifulSoup(r, 'html.parser')
			bib_link = bs.findAll('a', {'class': 'gs_citi'})[0].attrs['href']
			bib = self.__request_data({}, bib_link, header)
			return bib
		else:
			return -1

	def do_search_bd(self, kw):
		# 单条文献检索并格式化为BIBTEX格式 使用Baidu引擎
		# Stage 1 - search for the corresponding article
		kw = self.__clean_reflist(kw)   # 对输入文献串进行清洗
		params_1 = self.__encode_params(kw, param_opt=2)
		header = self.__header_bdscholar
		url = self.__url_bdscholar
		last_url = url + '?' + urllib.parse.urlencode(self.__last_params)
		header['Referer'] = last_url
		self.__last_params = params_1
		time.sleep(random.uniform(0.1,1.2))
		r = self.__request_data(params_1, url, header, need_proxy=False)
		if r.find('reqdata') >= 0:
			bs = BeautifulSoup(r, 'html.parser')
			if r.find('sc_q c-icon-shape-hover') >= 0:
				bd_params = {}
				reqdata = bs.findAll('a', {'class': 'sc_q c-icon-shape-hover'})[0].parent.parent.parent
				reqdata = reqdata.findAll('i', {'class': 'reqdata'})[0]
				bd_params['url'] = reqdata.attrs['url']
				bd_params['sign'] = bs.findAll('a', {'class': 'sc_q c-icon-shape-hover'})[0].attrs['data-sign']
				bd_params['diversion'] = reqdata.attrs['diversion']
				bd_params['allversion'] = reqdata.attrs['allversion']
			else:
				bd_params = {}
				bd_params['url'] = bs.findAll('i', {'class': 'reqdata'})[0].attrs['url']
				bd_params['sign'] = bs.findAll('a', {'class': 'sc_share'})[0].attrs['data-sign']
				bd_params['diversion'] = bs.findAll('i', {'class': 'reqdata'})[0].attrs['diversion']
				bd_params['allversion'] = bs.findAll('i', {'class': 'reqdata'})[0].attrs['allversion']
			# Stage 2 - get bib
			params_2 = self.__encode_params(kw, param_opt=5, bd_params=bd_params)   # 此处若调用opt.3，那么将会得到普通引用文本而非BIB
			bib = self.__request_data(params_2, self.__url_bdscholar_cite, header, need_proxy=False)
			return bib
		else:
			return -1

	def do_search_bd_json(self, kw):
		# 单条文献检索并格式化为BIBTEX格式 使用Baidu引擎
		# Stage 1 - search for the corresponding article
		kw = self.__clean_reflist(kw)  # 对输入文献串进行清洗
		params_1 = self.__encode_params(kw, param_opt=2)
		header = self.__header_bdscholar
		url = self.__url_bdscholar
		last_url = url + '?' + urllib.parse.urlencode(self.__last_params)
		header['Referer'] = last_url
		self.__last_params = params_1
		time.sleep(random.uniform(0.1, 1.2))
		r = self.__request_data(params_1, url, header, need_proxy=False)
		if r.find('reqdata') >= 0:
			bs = BeautifulSoup(r, 'html.parser')
			if r.find('sc_q c-icon-shape-hover') >= 0:
				bd_params = {}
				reqdata = bs.findAll('a', {'class': 'sc_q c-icon-shape-hover'})[0].parent.parent.parent
				reqdata = reqdata.findAll('i', {'class': 'reqdata'})[0]
				bd_params['url'] = reqdata.attrs['url']
				bd_params['sign'] = bs.findAll('a', {'class': 'sc_q c-icon-shape-hover'})[0].attrs['data-sign']
				bd_params['diversion'] = reqdata.attrs['diversion']
				bd_params['allversion'] = reqdata.attrs['allversion']
			else:
				bd_params = {}
				bd_params['url'] = bs.findAll('i', {'class': 'reqdata'})[0].attrs['url']
				bd_params['sign'] = bs.findAll('a', {'class': 'sc_share'})[0].attrs['data-sign']
				bd_params['diversion'] = bs.findAll('i', {'class': 'reqdata'})[0].attrs['diversion']
				bd_params['allversion'] = bs.findAll('i', {'class': 'reqdata'})[0].attrs['allversion']
			# Stage 2 - get bib
			params_2 = self.__encode_params(kw, param_opt=4, bd_params=bd_params)  # 此处若调用opt.3，那么将会得到普通引用文本而非BIB
			bib_str = self.__request_data(params_2, self.__url_bdscholar_cite, header, need_proxy=False)
			if int(json.loads(bib_str)['errno']) < 0:
				return -1
			bib_json = json.loads(bib_str)['sc_GBT7714']
			return bib_json
		else:
			return -1

	def do_bundle_search(self, kw_list):
		# 批量文献检索并格式化为BIBTEX格式列表
		self.__last_params = ''
		bibtex = []
		self.__wrong_reflist = []
		if len(kw_list) == 0:
			return -1
		count = 0
		for kw in kw_list:
			if self.__engine.lower() == 'google':
				bibitem = self.do_search_g(kw)
			else:
				if self.__need_str:
					bibitem = self.do_search_bd_json(kw)
				else:
					bibitem = self.do_search_bd(kw)
				if bibitem != -1:
					bibitem = bibitem.replace('\r\n','\n')
					bibitem = bibitem + '\n'
			count = count + 1
			if bibitem != -1:
				bibtex.append(bibitem)
				print('第'+str(count)+'项参考文献已匹配并录入成功...')
			else:
				self.__wrong_reflist.append(kw)
				print('- 第' + str(count) + '项参考文献匹配失败')
			time.sleep(random.uniform(4.0,9.5)) # 延迟，防止过快检索导致IP被Google封锁
		return bibtex

	def do_bundle_search_from_file(self, filename, save=False):
		try:
			f = open(filename)
			f.close()
		except FileNotFoundError:
			return -1
		except PermissionError:
			return -1
		with open(filename, 'r', encoding='UTF-8') as f:
			kw_list = f.readlines()
		bibtex = self.do_bundle_search(kw_list)
		if save:
			with open(filename + '.bib', 'a+', encoding='UTF-8') as f:
				f.writelines(bibtex)
		return bibtex

	def get_wrong_reflist(self):
		return self.__wrong_reflist

	def __request_data(self, params, url, header, need_proxy=True):
		try:
			proxies = {
				'http': self.__proxies,
				'https': self.__proxies
			}   # 挂上梯子代理
			if len(params)>0:
				if need_proxy:
					req = self.__session.get(url + '?' + urllib.parse.urlencode(params), headers=header, verify=False, proxies=proxies)
				else:
					req = self.__session.get(url + '?' + urllib.parse.urlencode(params), headers=header, verify=False)
			else:
				req = self.__session.get(url, headers=header, verify=False, proxies=proxies)
		except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError):
			raise Exception("链接超时或解包错误，请重试！")
		except:
			raise Exception("未知网络链接问题")
		return req.text

	def __encode_params(self, keyword, param_opt = 0, cid='123456789', bd_params={}):
		# 0,1 is for Google Scholar; 2,3,4,5 is for Baidu Xueshu
		if param_opt==0:
			params = {
				'hl': 'en',
				'as_sdt': '0,50',
				'q': keyword,
				'btnG': ''
			}
		elif param_opt==1:
			params = {
				'q': 'info:' + cid + ':scholar.google.com/',
				'output': 'cite',
				'scirp': '0',
				'hl': 'en'
			}
		elif param_opt==2:
			if self.__last_keyword == '':
				self.__last_keyword = keyword
			params = {
				'wd': keyword,
				'tn': 'SE_baiduxueshu_c1gjeupa',
				'cl': '3',
				'ie': 'utf-8',
				'bs': self.__last_keyword,
				'f': '8',
				'rsv_bp': '1',
				'rsv_sug2': '1',
				'sc_f_para': 'sc_tasktype={firstSimpleSearch}',
				'rsv_spt': '3'
			}
			self.__last_keyword = keyword
		elif param_opt==3:
			ts = str(int(time.time()))
			params = {
				'callback': 'jQuery1102029733501402635776_' + ts + '153',
				'sign': bd_params['sign'],
				'diversion': bd_params['diversion'],
				'url': bd_params['url'],
				'allversion': bd_params['allversion'],
				't': 'cite',
				'_': ts + '156',
			}
		elif param_opt==4:
			params = {
				'': '',
				'url': bd_params['url'],
				'sign': bd_params['sign'],
				'diversion': bd_params['diversion'],
				't': 'cite',
			}
		elif param_opt==5:
			params = {
				'': '',
				'url': bd_params['url'],
				'sign': bd_params['sign'],
				'diversion': bd_params['diversion'],
				't': 'bib',
			}
		return params

	def __urlencode(self, str):
		reprStr = repr(str).replace(r'\x', '%').lower()
		return reprStr[1:-1]

	def __clean_reflist(self, kw):
		# 清洗待输入的文献条目
		# Step 1 - Index Indicator
		if str(kw).find('[') >= 0 and str(kw).find(']') >= 0:
			# 存在标号，进行清理
			re_index = re.compile(r'\[\w+\]')
			kw = re_index.sub('', kw)
		kw = kw.strip()
		kw = kw.split('_')
		if len(kw) == 2:
			l1 = len(kw[0])
			l2 = len(kw[1])
			if kw[0].find(',') >= 0 and l1 < l2:
				if self.__contain_zh(kw[1]):
					return kw[1] + ' ' + kw[0]
				else:
					return kw[1]
			if kw[1].find(',') >= 0 and l1 > l2:
				if self.__contain_zh(kw[0]):
					return kw[0] + ' ' + kw[1]
				else:
					return kw[0]
			if l1 > l2:
				if self.__contain_zh(kw[0]):
					return kw[0] + ' ' + kw[1]
				else:
					return kw[0]
			else:
				if self.__contain_zh(kw[1]):
					return kw[1] + ' ' + kw[0]
				else:
					return kw[1]
		else:
			return kw[0]

	def __contain_zh(word):
		zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
		word = word.decode()
		match = zh_pattern.search(word)
		return match

