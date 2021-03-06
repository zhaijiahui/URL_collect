# -*- coding:utf-8 -*-
# run python3
# author: zhaijiahui
import requests
import re
import getopt,sys
import time


def please_geturl(url,s_url,sleeptime): # 获取页面链接
	for lurl in url:
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
		}
		try:
			r = requests.get(lurl,verify=True,headers=headers)
		except Exception as e:
			print('[*]	' + lurl+'	链接访问出错......')
			continue
		
		
		try:
			try:
				html = r.content.decode('gbk')
			except UnicodeDecodeError:
				html = r.content.decode('utf-8')
		except UnicodeDecodeError:
			print('[*]	' + lurl +'   链接内容无法解析......')
			continue
		
		# print(html)
		get_url2 = get_url3 = get_url4 = get_url5 = get_url6 = get_url7 = []
		# ---------------------页面URL-------------------------------
		get_url2 = re.findall('href="([^,\'\"\(;{]{9,}?)"',html)
		get_url3 = re.findall('href=\'([^,\'\"\(;{]{9,}?)\'',html)
		get_url4 = re.findall('src="([^,\'\"\(;{]{9,}?)"',html)
		get_url5 = re.findall('src=\'([^,\'\"\(;{]{9,}?)\'',html)
		get_url6 = re.findall('data-url=\'([^,\'\"\(;{]{9,}?)\'',html)
		get_url7 = re.findall('data-url="([^,\'\"\(;{]{9,}?)"',html)
		# ----------------------页面IP--------------------------------
		ipv4 = re.findall('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$',html)
		# ----------------------包含绝对路径---------------------------
		cmd = re.findall('([A-Z]:[\\/][^,\'\"\(;{]{9,}?)"',html)
		cmd1 = re.findall('\'([A-Z]:[\\/][^,\'\"\(;{]{9,}?)\'',html)
		mingan = []
		mingan.extend(ipv4)
		mingan.extend(cmd)
		mingan.extend(cmd1)

		mingan = list(set(mingan))
		# (?:href=\").+?(?=\")
		# get_url = re.findall('(http://.+?\..+?\..*)\'',html)
		# print(get_url2,get_url3,get_url4,get_url5)
		get_url2.extend(get_url3) # 合并url链接
		get_url2.extend(get_url4)
		get_url2.extend(get_url5)
		get_url2.extend(get_url6)
		get_url2.extend(get_url7)

		get_url = list(set(get_url2))
		# print(get_url)
		get_url_list = []
		suffix = ['jpg','mp4','gif','png','gif-s1','jpg-s1','png-s1','ico','swf','doc','docx','xls']
		static = ['html','js','css']
		dynamics = ['?', 'asp', 'php', 'jsp','aspx','jspx','shtml']
		for i in get_url:
			if '../' in i: # ../../../js/MSClass.js
				rurl=lurl.split('/')
				i=i.split('/')
				l1 = len(rurl)
				l2 = len(i)
				bb= i.count('..')
				temp = ''
				for x in range(l1-bb): # 拼接绝对路径，合成完整URL
					temp = temp+rurl[x]+'/'
					# print(url[x],end='/')
				for y in range(bb,l2):
					temp = temp+i[y]+'/'
					# print(i[y],end='/')
				temp = temp[:-1]
				if '../' in temp:
					temp = temp[:-3]
				# print(temp)
				get_url_list.append(temp)
			# elif lurl in i: # 
			# 	get_url_list.append(i)
			elif 'http://' in i:            # http://www.xxx.com/main.js
				get_url_list.append(i)
			elif 'https://' in i:          # https://www.xxx.com/main.js
				get_url_list.append(i)
			elif lurl.split('/')[-2] in i:  # http://xxx.cn/kpqyzx/ || /kpqyzx/js/MSClass.js
				temp = '/'.join(lurl.split('/')[:-2])+i
				get_url_list.append(temp)
			elif i[:2] == '//':            # //kpqyzx/js/MSClass.js
				temp  ='http:'+ i
				get_url_list.append(temp)
			elif i[:2] == './':            # ./kpqyzx/js/MSClass.js
				temp = s_url[:-1]+i[1:]
				get_url_list.append(temp)
			else:                             # /kpqyzx/js/MSClass.js
				temp = s_url[:-1]+i
				get_url_list.append(temp)
	# print(get_url_list)
	time.sleep(sleeptime)
	r_get_url_list = [] # 收集下一层所需的url
	if get_url_list: # 非空列表
		for x in get_url_list:
			if x.split('.')[-1] not in suffix: # 排除图片视频等资源文件
				r_get_url_list.append(x)
				for scr in dynamics:
					if scr in x:
						script_list.append(x)
				if '?' not in x:
					if x.split('.')[-1] in static:
						html_list.append(x)
					else:
						other_list.append(x)
			else:
				suffix_list.append(x)
	else:
		return r_get_url_list,script_list,html_list,other_list,suffix_list,mingan
	return r_get_url_list,script_list,html_list,other_list,suffix_list,mingan
		

if __name__ == '__main__':
	deep = 1 # 深度
	writefile = 0 # 是否保存文件
	sleep = 0 # 睡眠时间
	# 列表声明
	suffix_list = []
	script_list = []
	other_list = []
	html_list = []
	# 多深度列表声明
	n_suffix_list = []
	n_script_list = []
	n_other_list = []
	n_html_list = []

	Usage='''
# ------------------------------
# URL collect by zhaijiahui
# ------------------------------
-u  Input your domain
-d  Crawl depth
-o  Save result
-s  sleep time,Prevent requests too fast
Usage: get_url2.py -u http://www.target.com/ -d 2 -s 2 -o'''
	if not len(sys.argv[1:]):
		print(Usage)
		exit()
	# url= ["http://www.1993s.top/"]
	# s_url = "http://www.1993s.top/"
	try:
		options,args = getopt.getopt(sys.argv[1:],"hu:d:os:",["help","url=","deep=","out","sleep"])
	except getopt.GetoptError:
		exit()
	for option,value in options:
		if option in ("-h","--help"):
			print(Usage)
			exit()
		if option in ("-u","--url"):
			if value[-1] == '/':
				url = [value]
				s_url = value
			else:
				url = [value+'/']
				s_url = value+'/'
		if option in ("-d","--deep"):
			deep = int(value)
		if option in ("-s","--sleep"):
			sleep = int(value)
		if option in ("-o","--out"):
			writefile = 1
	for rd in range(deep):
		print('['+time.ctime()+']   抓取深度   ' + str(rd+1))
		r_get_url_list,script_list,html_list,other_list,suffix_list,mingan = please_geturl(url,s_url,sleep)
		# if r_get_url_list == None:
		# 	break
		url = r_get_url_list
		n_suffix_list.extend(suffix_list)
		n_script_list.extend(script_list)
		n_other_list.extend(other_list)
		n_html_list.extend(html_list)
	if writefile == 1:
		with open(time.ctime()+'_'+s_url+'_result.txt','w+') as f:
			f.write('----------------------------脚本或可传参目录------------------------------\n')
			for i in list(set(script_list)):
				f.write(i+'\n')
			f.write('-------------------------------静态目录----------------------------------\n')
			for i in list(set(html_list)):
				f.write(i+'\n')
			f.write('-------------------------------其他目录----------------------------------\n')
			for i in list(set(other_list)):
				f.write(i+'\n')
			f.write('---------------------------图片视频等资源目录-----------------------------\n')	
			for i in list(set(suffix_list)):
				f.write(i+'\n')
	
	print('----------------------------脚本或可传参目录------------------------------')
	for i in list(set(script_list)):
		print(i)
	print('-------------------------------静态目录----------------------------------')
	for i in list(set(html_list)):
		print(i)
	print('-------------------------------其他目录----------------------------------')
	for i in list(set(other_list)):
		print(i)
	print('---------------------------图片视频等资源目录-----------------------------')
	for i in list(set(suffix_list)):
		print(i)
	print('-------------------------------敏感路径----------------------------------')
	for i in mingan:
		print(i)
