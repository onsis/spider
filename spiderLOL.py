# -*- coding:utf-8 -*-
import urllib2
import os
import re

url = 'http://www.dytt8.net'  #这是电影天堂最新电影的网站
conent = urllib2.urlopen(url)
print  conent
conent =  conent.read()
print  conent
conent = conent.decode('gb2312','ignore').encode('utf-8','ignore')  
print  conent
#这个‘ignore’差点就忘了，主要是对一些可以忽略的参数进行编码忽略，下午一直没想起来总是出错
#pattern = re.compile ('<div class="title_all"><h1><font color=#008800>.*?</a>></font></h1></div>'+
#                     '(.*?)<td height="25" align="center" bgcolor="#F4FAE2"> ',re.S)
#pattern = re.compile('[/html/gndy/]')
#print  pattern
#items = re.findall(pattern,conent)#先把含有最新电影的网页代码选出来，再进行下一次筛选


#str = ''.join(items)
#pattern = re.compile ('a',re.S)
#print pattern
#news = re.findall(pattern, conent)
#file = open('g:/new movie.txt','w')#创建一个txt文件保存爬到的电影名，简介，下载页面
#file.write('最新电影：\n\n')
#for  j in news:
#        file.write('片名：'+j[1]+'\n'+'简介：'+j[2]+'\n'+'下载地址：'+'http://www.ygdy8.net'+j[0]+'\n'+'\n')
#file.close()