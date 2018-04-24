#!/usr/bin/env python
#encoding:utf-8
content="""
<p id='i1' a='123' b='fdasfas'>
    <script>alert(123)</script>
</p>
<p id='i2'>
<div>
    <p>fdasfdsafa</p>
</div>
    <img id='i3' src="/static/imgs/1.png" alt="" />
</p>

"""

from bs4 import BeautifulSoup
soup=BeautifulSoup(content,'html.parser')
#tag=soup.find(name='img')
# tag=soup.find(name='p')
# sc=tag.find(name='script')
# print(sc)
# print(tag)
# v=soup.find(attrs={'id':'i2'})
# v=soup.find(name='p',attrs={'id':'i2'})


# #设置白名单
# valid_tag=['p','img','div']
# # v=soup.find_all(name='p')
# tags=soup.find_all()#所有的标签
#
# for tag in tags:
#     print(tag.name) #打印标签名
#     if tag.name not in valid_tag:
#         # tag.clear()  #删除内容
#         tag.decompose()  #把标签都删掉
#
#
# # print(tags)
# print(soup.decode())  #取字符串
# content_str=soup.decode()


#删除不要的属性和标签
tags=soup.find_all()#所有的标签
valid_dict={
    'p':['class','id'],
    'img':['src'],
    'div':['class']
}

for tag in tags:
    if tag.name not in valid_dict:
        tag.decompose()  #把标签都删掉
    if tag.attrs:
        for k in list(tag.attrs.keys()): #获取标签属性的key值
            if k not in valid_dict[tag.name]:
                del tag.attrs[k]

print(soup.decode())