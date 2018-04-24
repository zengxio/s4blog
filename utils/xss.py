#!/usr/bin/env python
#encoding:utf-8
from bs4 import BeautifulSoup
def xss(old):
    soup = BeautifulSoup(old, 'html.parser')
    tags = soup.find_all()  # 所有的标签
    valid_dict = {
        'p': ['class', 'id'],
        'img': ['src'],
        'div': ['class']
    }

    for tag in tags:
        if tag.name not in valid_dict:
            tag.decompose()  # 把标签都删掉
        if tag.attrs:
            for k in list(tag.attrs.keys()):  # 获取标签属性的key值
                if k not in valid_dict[tag.name]:
                    del tag.attrs[k]

    content_str = soup.decode()
    return content_str