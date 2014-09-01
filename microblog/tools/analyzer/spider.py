# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
from pymongo import MongoClient
from weibo import APIClient

class AccessTockenDoesNotExists(Exception):
    pass


class WeiboSpider(object):

    def __init__(self, APP_KEY, APP_SECRET, CALLBACK_URL):
        self.client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        self.mongo_client = MongoClient(tz_aware=True)
        self.db = self.mongo_client['weibo_analyzer']
        self.status_collection = self.db['status']      # 微博集合

    def authorize(self):
        try:
            access_token, expires_in = self.load_access_token()
            self.client.set_access_token(access_token, expires_in)
        except AccessTockenDoesNotExists as e:
            print('授权文件不存在，将重新授权。')
        # print(self.client.access_token, self.client.is_expires())
        if self.client.is_expires():
            # 过期，重新授权
            url = self.client.get_authorize_url()
            print('请访问下面的链接获取授权码：')
            print(url)
            # 获取URL参数code:
            print('请输入授权码：')
            code = raw_input()
            r = self.client.request_access_token(code)
            access_token = r.access_token # 新浪返回的token，类似abc123xyz456
            expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
            # TODO: 在此可保存access token
            self.client.set_access_token(access_token, expires_in)
            self.save_access_token()

    def save_access_token(self, filename='access_token'):
        f = open(filename, 'w')
        f.write(self.client.access_token + '\n' + str(self.client.expires))
        f.close()

    def load_access_token(self, filename='access_token'):
        if not os.path.exists(filename):
            raise AccessTockenDoesNotExists

        f = open(filename, 'r')
        access_token = f.readline().strip()
        expires_in = f.readline().strip()
        f.close()
        return (access_token, expires_in)

    def crawl(self):
        data = self.client.statuses.public_timeline.get(
            access_token=self.client.access_token,
            count=200,
        )
        statuses = data['statuses']
        crawled_num = 0
        for status in statuses:
            write_result = self.status_collection.update({'id': status['id']}, {'$set': status}, upsert=True)
            if not write_result['updatedExisting']:
                crawled_num += 1
        return crawled_num

# print client.statuses.user_timeline.get()
# print client.statuses.update.post(status='测试OAuth 2.0发微博')
# print client.statuses.upload.post(status='测试OAuth 2.0带图片发微博', pic=open('test.png'))


APP_KEY = '1150333334' # app key
APP_SECRET = '011f73cbde90d0ac73f8cf00b1c27908' # app secret
CALLBACK_URL = 'http://vieboo.duapp.com' # callback url


from time import sleep

if __name__ == '__main__':
    spider = WeiboSpider(APP_KEY, APP_SECRET, CALLBACK_URL)
    spider.authorize()
    # spider.load_access_token()
    while True:
        crawled_num = spider.crawl()
        print('crawled {0} statuses.'.format(crawled_num))
        sleep(5)
