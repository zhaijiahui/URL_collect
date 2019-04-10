# URL_collect

用于爬取网站源码内所有连接，并对爬取结果进行分类。


#---------------------------

#URL collect by zhaijiahui

#---------------------------


-u  Input your domain

-d  Crawl depth

-o  Save result

-s  Prevent requests too fast

Usage: 
	get_url.py -u http://www.target.com/ -d 2
	get_url.py -u http://www.target.com/ -d 2 -s 2 -o



##  bug

+ 1 修复 http://kpjy.kaiping.gov.cn/kpqyzx/ || /kpqyzx/js/MSClass.js  此类型爬取异常
+ 2 url 拼接逻辑问题





