from django.test import TestCase
from ..models import Reference
from datetime import datetime
from spider.forms import LinkForm

class ReferenceTestCase(TestCase):
    def setUp(self):
        Reference.objects.create(crawled_uri="https://www.sumitraj.in")
        Reference.objects.create(crawled_uri="https://blog.sumitraj.in")

    def test_reference_created(self):
        """Animals that can speak are correctly identified"""
        site1 = Reference.objects.get(crawled_uri="https://www.sumitraj.in")
        site2 = Reference.objects.get(crawled_uri="https://blog.sumitraj.in")

        self.assertTrue(isinstance(site1.url_id, int))
        self.assertTrue(isinstance(site2.created_at, datetime))


class LinkFormTestCase(TestCase):
    def test_linkform(self):
        form_data = {'link': 'https://sumitraj.in'}
        form = LinkForm(data=form_data)
        self.assertTrue(form.is_valid())

class UploadS3TestCase(TestCase):
	pass