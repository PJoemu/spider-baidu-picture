#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: x.huang
@date:17-6-8
"""
# 获取每页图片的访问链接
from __future__ import print_function

import os
import re
import traceback
from urllib.parse import quote

import gevent
import requests
from gevent import monkey
from requests import Timeout

monkey.patch_all()

DIST_DIR = '/home/huangxing/resource/picture/pict_baidu/'


def get_page(key_word=None, width='', height=''):
    if key_word is None:
        print('key work can not empty.')
        return

    global DIST_DIR

    DIST_DIR = os.path.join(DIST_DIR, '%s_%s_%s' % (key_word, width, height))

    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

    urls = [
        'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={}&pn={}&gsm=3c00000000003c&width={}&height={}'.format(
            quote(key_word), num, width, height) for num in range(0, 20000, 20)]
    for url in urls:
        print(url)
        get_img_link(url)


# 从网页中获取每个图片的访问链接
def get_img_link(url):
    if url.endswith('gif'):
        return
    r = requests.get(url)
    # print(r.encoding)
    r.encoding = 'utf-8'
    html_code = r.text
    reg = re.compile(r'"objURL":"(.*?)"')
    imgs = re.findall(reg, html_code)
    # print(imgs)
    jobs = list()
    for img in imgs:
        # print(img)
        jobs.append(gevent.spawn(down_img, img))
    gevent.joinall(jobs)


# 图片下载保存再本地
def down_img(url):
    try:
        web_data = requests.get(url, timeout=3)
        gevent.sleep(0)
        print(url, 'start')
        filename = url.split('/')[-1]
        targetfile = os.path.join(DIST_DIR, filename)

        with open(targetfile, 'wb') as f:
            f.write(web_data.content)
            print(url, 'done')

    except Timeout as e:
        pass
    except Exception as e:
        print(traceback.format_exc())


if __name__ == '__main__':
    import sys

    key_word = None
    try:
        key_word = sys.argv[1]
        width = sys.argv[2]
        height = sys.argv[3]
    except IndexError as e:
        width = ''
        height = ''
        pass
    if not key_word:
        print('请输入搜索关键字！')
        print('Usage： ')
        print("     python spider.py key_word width height")
        print("     python spider.py '美女' 512 512")
    else:
        print(key_word)
        print(width)
        print(height)
        get_page(key_word, width, height)
