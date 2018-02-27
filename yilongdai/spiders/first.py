# -*- coding: utf-8 -*-
import json
import sys
import sqlite3

import scrapy
from scrapy.http import Request

from yilongdai.items import YilongdaiItem
from yilongdai.settings import DataBase

reload(sys)
sys.setdefaultencoding('utf-8')

class FirstSpider(scrapy.Spider):
    name = 'first'
    allowed_domains = ['eloancn.com']
    list_url = r"https://licai.eloancn.com/pcgway/gateway/v1/01?pageNo={}&platform=5&requesturl=%2Fappwmps%2Fapp004%2Fv2%2F01&v=0.26863688930572927"
    detail_url = r"https://www.eloancn.com/getTenderInfoByWid.action?page={0}&wid={1}"
    response_url = r"http://www.eloancn.com//fenye.action?fpage={0}&wid={1}"
    ls_page_count = 1
    resp_page_count = 1

    def __init__(self):
        super(self.__class__, self).__init__()
        self.conn = sqlite3.connect(DataBase)
        self.cur = self.conn.cursor()
        self.list = set(self.cur.execute('SELECT [编号] FROM Content WHERE [标题] NOT NULL;').fetchall())

    def start_requests(self):
        yield Request(url=self.list_url.format(self.ls_page_count),
                       callback=self.second_requests) 

    def second_requests(self, response):
        data = json.loads(response.text).get('data')
        page = data['page']
        total = data['total']

        for info in data['data']:
            item = YilongdaiItem()
            item['index'] = info['idNoDes']
            item['progressBar'] = info['progressBar']

            yield Request(url=self.response_url.format(self.resp_page_count, item['index']),
                          callback=self.response_parse,
                          meta={'item':item}
                          )

        if total > page:
            self.ls_page_count += 1
            yield Request(url=self.list_url.format(self.ls_page_count),
                          callback = self.second_requests
                          )

    def response_parse(self, response):
        data = json.loads(response.text).get('pageBuyRecordList').get('list')
        item = response.meta['item']
        item['time'] = data[0]['strCdate']
        item['create_time'] = data[-1]['strCdate']

        yield Request(url=self.detail_url.format(1, item['index']),
                      callback=self.detail_parse, 
                      meta={'item':item}
                      )

    def detail_parse(self, response):
        data = json.loads(response.text).get('pageWmpsBuyRecordList').get('list')
        total = json.loads(response.text).get('pageWmpsBuyRecordList').get('totalPage')
        page = json.loads(response.text).get('pageWmpsBuyRecordList').get('index')
        item = response.meta['item']

        for info in data:
            if (str(info['tid']),) not in self.list:
                item['amount'] = info['amount']
                item['interestrate'] = float(info['interestrate']*100)
                item['detailsTitle'] = info['detailsTitle']
                item['tid'] = info['tid']
                item['authod_userName'] = info['userName']
                item['authod_userId'] = info['userId']
                item['phases'] = info['phases']
                
                yield item

        if total > page:
            item = response.meta['item']
            yield Request(url=self.detail_url.format(page+1, item['index']),
                          callback=self.detail_parse,
                          meta={'item':item})

    def parse(self, response):
        pass
