import re
import json

try:
	from urllib.parse import urljoin
except ImportError:
	 from urlparse import urljoin

import scrapy
from scrapy.http.request import Request
from scrapy.linkextractors import LinkExtractor

from ..utils.clean import clean_emails
from ..utils.aws import get_boto_session, upload_to_s3



class GenericSpider(scrapy.Spider):
	name = 'genericspider'

	def __init__(self, *args, **kwargs):
		self.myurl = kwargs.get('myurl', "https://sumitraj.in")
		self.url_id = kwargs.get('url_id', 999999)

		super(GenericSpider, self).__init__(*args, **kwargs)

	def start_requests(self):
		yield Request(self.myurl, self.parse)

	def extract_link(self, response):
		"""Returns all links from response object"""

		le = LinkExtractor() # empty for getting everything, check different options on documentation
		all_links = []
		
		for link in le.extract_links(response):
			all_links.append(link.url)


		all_links_endpoint = list(filter(lambda x: x.startswith(response.url), all_links))
		return list(set(all_links_endpoint))

	def extract_emails(self, response):
		"""Returns all emails from response object"""

		emails = re.findall(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]+', response.text)
		print(emails, "emails")
		emails = clean_emails(emails)
		return list(set(emails))

	def extract_meta_tags(self, response):
		"""Returns a tuple of meta keywords and description"""

		meta_keywords = meta_desc = None
		meta_keywords = response.xpath("//meta[@name='keywords']/@content")
		meta_desc = response.xpath("//meta[@name='description']/@content")
		
		if meta_keywords:
			meta_keywords = meta_keywords[0].extract()

		if meta_desc:
			meta_desc = meta_desc[0].extract()
		
		return meta_keywords, meta_desc
	
	def extract_images(self, response):
		"""Returns all images from response object"""
		img_urls = [urljoin(response.url, src)
						for src in response.xpath('//img/@src').extract()]
		return list(set(img_urls))
	
	def parse(self, response):
		"""Parsing of the response data"""
		title = response.xpath('//title/text()').get()
		all_links = self.extract_link(response)
		all_emails = self.extract_emails(response)
		meta_keywords, meta_desc = self.extract_meta_tags(response)
		img_urls = self.extract_images(response)

		res = {'title': title, 
			   'text': " ".join(response.xpath('//body//p/text()').extract()),
			   # 'html': response.text,
			   'all_links': all_links,
			   'all_emails': all_emails,
			   'meta_keywords': str(meta_keywords),
			   'meta_desc': str(meta_desc),
			   'images': img_urls,
			   'url_id': self.url_id
			   }
		# for k in res:
		# 	print("here", k, type(res[k]))
		# # print(res, "before sending")
		
		file_name = str(self.url_id) + '.txt'
		public_link = upload_to_s3(response.text, file_name, 'crawled-htmls')
		res['s3_link'] = "https://crawled-htmls.s3.amazonaws.com/" + file_name
		
		self.store_in_dynamodb(res)

		return res

	def store_in_dynamodb(self, json):
		"""Stores data in DynamoDB"""
		
		session = get_boto_session()
		dynamodb = session.resource('dynamodb', region_name='us-east-1')   
		leap_finance = dynamodb.Table('leap_finance')
		leap_finance.put_item(Item=json)
