from scrapy.linkextractors import LinkExtractor
import scrapy
import re
import json

from scrapy.http.request import Request

from ..utils.clean import clean_emails, clean_images
from ..utils.aws import get_boto_session, upload_to_s3

try:
	from urllib.parse import urljoin
except ImportError:
	 from urlparse import urljoin

class GenericSpider(scrapy.Spider):
	name = 'genericspider'
	# start_urls = ['https://www.sumitraj.in']

	def __init__(self, *args, **kwargs):
		self.myurl = kwargs.get('myurl', "https://sumitraj.in")
		self.url_id = kwargs.get('url_id', 999999)

		super(GenericSpider, self).__init__(*args, **kwargs)

	def start_requests(self):
		yield Request(self.myurl, self.parse)

	def extract_link(self, response):
		le = LinkExtractor() # empty for getting everything, check different options on documentation
		all_links = []
		
		for link in le.extract_links(response):
			# print(link, "link")
			all_links.append(link.url)
		# print(response.url, "response.url")
		# print(all_links, "all_links")

		all_links_endpoint = list(filter(lambda x: x.startswith(response.url), all_links))
		# print(all_links_endpoint, "all_links_endpoint")
		# print(list(set(all_links_endpoint)),  "set all_links_endpoint")
		return list(set(all_links_endpoint))

	def extract_emails(self, response):
		emails = re.findall(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]+', response.text)
		print(emails, "emails")
		emails = clean_emails(emails)
		return list(set(emails))

	def extract_meta_tags(self, response):
		meta_keywords = meta_desc = None
		meta_keywords = response.xpath("//meta[@name='keywords']/@content")
		meta_desc = response.xpath("//meta[@name='description']/@content")
		
		if meta_keywords:
			meta_keywords = meta_keywords[0].extract()

		if meta_desc:
			meta_desc = meta_desc[0].extract()
		
		return meta_keywords, meta_desc
	
	def extract_images(self, response):
		img_urls = [urljoin(response.url, src)
						for src in response.xpath('//img/@src').extract()]
		img_urls = clean_images(img_urls)
		return list(set(img_urls))
	
	def parse(self, response):
		title = response.xpath('//title/text()').get()
		# import pdb; pdb.set_trace()
		# print(response.text, "res")
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
		for k in res:
			print("here", k, type(res[k]))
		# print(res, "before sending")
		file_name = str(self.url_id) + '.txt'
		public_link = upload_to_s3(response.text, file_name, 'crawled-htmls')
		res['s3_link'] = "https://crawled-htmls.s3.amazonaws.com/" + file_name
		self.store_in_dynamodb(res)

		return res

	def store_in_dynamodb(self, json):
		session = get_boto_session()
		dynamodb = session.resource('dynamodb', region_name='us-east-1')   
		leap_finance = dynamodb.Table('leap_finance')
		leap_finance.put_item(Item=json)

#9aca6e3c41944832a915fbed2eb36f8e

# curl -u 9aca6e3c41944832a915fbed2eb36f8e: https://app.scrapinghub.com/api/run.json -d project=417546 -d spider=genericspider
# curl -u 9aca6e3c41944832a915fbed2eb36f8e: https://storage.scrapinghub.com/items/417546/1/1


# Run your spiders at: https://app.scrapinghub.com/p/417546/

# scrapy runspider extractor/spiders/myspider.py 


# curl -u 9aca6e3c41944832a915fbed2eb36f8e: https://storage.scrapinghub.com/items/417546/1/3/

# scrapy parse --spider=genericspider http://bigrock.in

# curl -u 9aca6e3c41944832a915fbed2eb36f8e: https://storage.scrapinghub.com/logs/417546/1/3/

