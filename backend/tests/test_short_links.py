import json
import logging
import pytest

from django.test import TestCase
logger = logging.getLogger(__name__)
from front.services import UrlsController
@pytest.mark.django_db
# @override_settings(SENSITIVE_DB_CONN=FAKE_REDIS_CONN)
class TestClient(TestCase):

    def setUp(self):
        file = open('common/fixtures/dummy_urls.json', 'r')
        self.test_urls = json.load(file)

    def test_url_controller(self):
        print("test")
        assert 1 == 2
