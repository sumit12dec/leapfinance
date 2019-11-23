from datetime import datetime
from urllib.parse import urlencode

import requests
from django.test import TestCase, Client

from ..models import Reference
from spider.forms import LinkForm
from extractor.utils.aws import upload_to_s3
from spider.utils import get_item

class ReferenceTestCase(TestCase):
	def setUp(self):
		Reference.objects.create(crawled_uri="https://www.sumitraj.in")
		Reference.objects.create(crawled_uri="https://blog.sumitraj.in")

	def test_reference_created(self):
		"""Reference object created in SQL DB"""
		site1 = Reference.objects.get(crawled_uri="https://www.sumitraj.in")
		site2 = Reference.objects.get(crawled_uri="https://blog.sumitraj.in")

		self.assertTrue(isinstance(site1.url_id, int))
		self.assertTrue(isinstance(site2.created_at, datetime))


class LinkFormTestCase(TestCase):
	def test_linkform(self):
		"""Check Link submission form validation"""
		form_data = {'link': 'https://sumitraj.in'}
		form = LinkForm(data=form_data)
		self.assertTrue(form.is_valid())

class UploadS3TestCase(TestCase):
	def test_upload_html(self):
		"""Test HTML file upload to S3 budket successfully"""
		file_name = 'test123.txt'
		public_link = upload_to_s3('<html><body></body></html>', file_name, 'crawled-htmls')
		s3_url = "https://crawled-htmls.s3.amazonaws.com/" + file_name
		self.assertEqual(requests.get(s3_url).status_code, 200)


class ScrapingTestCase(TestCase):
	def test_scraping(self):
		"""Test scraping happend using AWS Lambda"""
		client = Client(HTTP_USER_AGENT='Mozilla/5.0')
		data = urlencode({"link": "https://sumitraj.in"})
		response = client.post("/spider/", data, content_type="application/x-www-form-urlencoded")
		self.assertEqual(response.status_code, 200)

	def test_storage_dynamodb(self):
		"""Test Scraped data successfully stored in DynamoDB"""
		response = get_item(40)
		self.assertEqual(response.get('url_id'), '40')
