#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Doc description: 获取qiushibaike的内容'

__author__ = 'HisenLee'

import urllib.request
import re

def getcontent(url, pageIndex):	
	headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0")
	opener = urllib.request.build_opener()
	opener.addheaders = [headers]
	urllib.request.install_opener(opener)
	html = urllib.request.urlopen(url).read().decode("utf-8")
	# 第一层匹配，先剔除掉网页起始端无用的信息  .+?懒惰匹配至少一个任意单个字符 re.S 让点匹配包括换行符
	# A.*?B 包括A和B  A.*?(?=B) 包括A不包括B  (?<=A).*?(?=B) 不包括A也不包括B
	pattern1 = '"content-left".+?"pagination"'
	result1 = re.compile(pattern1, re.S).findall(html)
	result1 = result1[0]
	# 第二层匹配，取出用户信息  re.S 让点匹配包括换行符
	patternForUser = '(?<=<h2>).+?(?=</h2>)'
	userList = re.compile(patternForUser, re.S).findall(result1)
	# 第三层匹配，取出内容 \s*? 懒惰匹配任意空白符{0,} re.S 让点匹配包括换行符
	patternForContent = '<div class="content">\s*?<span>.+?</span>\s*?</div>'
	contentList = re.compile(patternForContent, re.S).findall(result1)
	print("正在获取第" + str(pageIndex) + "页的数据，该页共有" + str(len(contentList)) + "条数据" )
	# 输出每个用户对应的内容
	index = 0
	for content in contentList:
		print("用户" + userList[index] + "的内容是:\n" + content + "\n")
		index+=1

for pageIndex in range(1, 30):
	url = "http://www.qiushibaike.com/8hr/page/" + str(pageIndex)
	getcontent(url, pageIndex)
