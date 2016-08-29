# -*- coding:utf-8 -*-
import urllib2
import os
import re


url = 'http://www.dytt8.net'  #这是电影天堂最新电影的网站
conent = urllib2.urlopen(url)
conent =  conent.read()
conent = conent.decode('gb2312','ignore').encode('utf-8','ignore')  
pattern = re.compile('/html/gndy/dyzz/2016.*?.html',re.S)
news = re.findall(pattern, conent)
#print news
file = open('g:/new movie.txt','w')#创建一个txt文件保存爬到的电影名，简介，下载页面
file.write('最新电影：\n\n')
for  i in news:
    url= 'http://www.dytt8.net'+i
    opener=urllib2.urlopen(url)
    result = opener.read()
    result = result.decode('gb2312','ignore').encode('utf-8','ignore')
    #print result
    pattern = re.compile('"ftp://ygdy8:ygdy8@.*?.rmvb"',re.S)
    news = re.findall(pattern, result)
    for j in news:
        print j
        file.write('下载地址：'+j+'\n')


