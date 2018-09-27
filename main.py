# -*- coding:utf-8 -*-

import sengine
import sys
from sengine import *

def main():
	if False:
		# 这段是测试内容，实际运行不用管
		# Test Scenario 1
		se =  sengine(proxies='127.0.0.1:1080', engine='google')
		re = se.do_search_g('[5]	Slock.it Blockchain + IoT. [Online]. Available: https://slock.it/faq.md')
		print(re)
		# Test Scenario 2
		re = se.do_bundle_search_from_file('test.txt', save=True)
		print(re)
		print(se.get_wrong_reflist())
		# Test Scenario 3
		se =  sengine(proxies='127.0.0.1:1080', engine='baidu')
		re = se.do_search_bd('[1]	国外区块链技术的运用情况及相关启示_张波')
		print(re)
		# Test Scenario 4
		se = sengine(proxies='127.0.0.1:1080', engine='baidu')
		re = se.do_bundle_search_from_file('test.txt', save=True)
		print('导出完成...')

	# 用Python接受命令行输入

	print('欢迎使用参考文献格式化工具\n请注意：若您想要文本化输出，则输出内容非bibtex格式，可直接导入word进行编辑\n文本化输出虽简单快捷，但有较大可能无法匹配到合适文献。')
	if len(sys.argv) > 1:
		print('已识别输入文件...')
		se = sengine(proxies='127.0.0.1:1080', engine='baidu')
		for i in range(1, len(sys.argv)):
			re = se.do_bundle_search_from_file(sys.argv[i], save=True)
			print('导出完成...')
	else:
		file = input('请输入待处理参考文献文件名：')
		ns = input('请选择是否需要文本化输出（是输入Y，否输入N）：')
		if ns.lower().strip() == 'y':
			ns = True
		else:
			ns = False
		print('已识别输入文件...')
		se = sengine(proxies='127.0.0.1:1080', engine='baidu', need_str=ns)
		re = se.do_bundle_search_from_file(file, save=True)
		print('导出完成...')

if __name__ == '__main__':
	main()