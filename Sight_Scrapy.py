#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :2020/5/31 20:47
#@Author  :花神庙
#@FileName: Sight_Scrapy.py
#@Software: PyCharm

import json
import requests
import random
import time
import re
import pymysql
import pandas as pd
from requests.exceptions import RequestException

class SpiderSight():
    def __init__(self):
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

    #获取html
    def get_html(self,post_data):
        try:
            url='https://sec-m.ctrip.com/restapi/soa2/12530/json/viewCommentList'
            response = requests.post(url, data=json.dumps(post_data),headers=self.headers)
            random_int=random.randint(1,2)
            time.sleep(random_int)
            if response.status_code == 200:
                text=json.loads(response.text)
                return text
            return None
        except RequestException:
            return None
    def get_comment(self,page,sight_name):
        post_data = {
        "pageid": "10650000804",
        "viewid": "11793",
        "tagid": "0",
        "pagenum": str(page + 1),
        "pagesize": "50",
        "contentType": "json",
        "SortType": "1",
        "head": {
            "appid": "100013776",
            "cid": "09031037211035410190",
            "ctok": "",
            "cver": "1.0",
            "lang": "01",
            "sid": "8888",
            "syscode": "09",
            "auth": "",
            "extension": [
                {
                    "name": "protocal",
                    "value": "https"
                }
            ]
        },
        "ver": "7.10.3.0319180000"
        }
        data = self.get_html(post_data)
        comments = data['data']['comments']
        for i in comments:
            item={}
            id=i['id']
            user_name = i['uid']
            date = i['date']
            score = i['score']
            content = i['content']
            content = re.sub("&#x20;", "", content)
            content = re.sub("&#x0A;", "", content)
            item['id'] = id
            item['user_name']=user_name
            item['content'] = content
            item['score'] = score
            item['date'] = date
            item['sight_name']=sight_name
            self.into_sql(item)
    def into_sql(self,item):
        con=pymysql.connect(host='localhost',port=3306,user='root',password='123123',db='xiecheng',charset='utf8mb4')
        cur=con.cursor()
        try:
            sql="""insert into sight_comment(id,user_name,content,score,date,sight_name)values(%s,%s,%s,%s,%s,%s)"""
            lis=[item['id'],item['user_name'],item['content'],item['score'],item['date'],item['sight_name']]
            cur.execute(sql,lis)
            con.commit()
            print('用户：{}   评论：{}'.format(lis[1],lis[2]))
        except:
            con.rollback()
            print('数据存在')
        cur.close()
        con.close()

def main():
    spider=SpiderSight()
    pages=46
    sight_name='纳木措'
    for page in range(0,pages):
        print('*' * 10 + '正在获取第{}页评论'.format(page + 1) + '*' * 10)
        spider.get_comment(page,sight_name)
        print('\n')

if __name__ == '__main__':
    main()