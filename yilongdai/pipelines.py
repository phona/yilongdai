# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import sys

from yilongdai.settings import DataBase

reload(sys)
sys.setdefaultencoding('utf-8')

class YilongdaiPipeline(object):

	def __init__(self):
		self.con = sqlite3.connect(DataBase)
		self.cur = self.con.cursor()

	def process_item(self, item, spider):

		author = str(item['authod_userId']) + str(item['authod_userName'])
		period = str(item['phases']) + '天'
		webid = 'https://www.eloancn.com/new/loadWmpsTenderDetails.action?tenderid=' + str(item['tid'])


		lis = '\
				[标题],[编号],[借款金额],[年利率],[借款期限], \
				[发标时间],[完成度],[时间], \
				[已采],[已发],[网址],[网站编号],[作者], [内容]'
		values = "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" %(
				item['detailsTitle'], item['tid'], 
				item['amount'], item['interestrate'],
				period, item['create_time'], 
				item['progressBar'], item['time'], 
				1, 0, webid, 134, author, item['index']
				)


		sql = "INSERT INTO Content (%s) VALUES (%s)" % (lis, values)
		self.cur.execute(sql)
		self.con.commit()
		return item

	def close_spider(self, spider):
		self.cur.close()
		self.con.close()
