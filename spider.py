#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: x.huang
@date:17-6-8
"""
# 获取每页图片的访问链接
import os
import re
import requests
import traceback
import urllib2
from requests import Timeout


def get_page(key_word=None, width='', height=''):
    if key_word is None:
        print 'key work can not empty.'
        return

    global DIST_DIR
    DIST_DIR = '/home/huangxing/resource/picture/pict_baidu/'

    DIST_DIR = os.path.join(DIST_DIR, '%s_%s_%s' % (key_word, width, height))

    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

    urls = [
        'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={}&pn={}&gsm=3c00000000003c&width={}&height={}'.format(
            urllib2.quote(key_word), num, width, height) for num in range(0, 20000, 20)]
    for url in urls:
        print(url)
        get_img_link(url)


# 从网页中获取每个图片的访问链接
def get_img_link(url):
    r = requests.get(url)
    # print(r.encoding)
    r.encoding = 'utf-8'
    html_code = r.text
    reg = re.compile(r'"objURL":"(.*?)"')
    imgs = re.findall(reg, html_code)
    # print(imgs)
    for img in imgs:
        # print(img)
        down_img(img)


# 图片下载保存再本地
def down_img(url):
    try:
        web_data = requests.get(url, timeout=3)
        filename = url.split('/')[-1]
        targetfile = os.path.join(DIST_DIR, filename.encode('utf-8'))

        with open(targetfile, 'wb') as f:
            f.write(web_data.content)
    except Timeout as e:
        pass
    except Exception as e:
        print traceback.format_exc()


if __name__ == '__main__':
    import sys

    try:
        key_word = sys.argv[1]
        width = sys.argv[2]
        height = sys.argv[3]
    except IndexError as e:
        width = ''
        height = ''
        pass
    print key_word
    print width
    print height
    get_page(key_word, width, height)
