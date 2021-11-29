import json
import logging
from django.forms import ValidationError
import pytest
import fakeredis

from django.test import TestCase
logger = logging.getLogger(__name__)
from front.services import UrlsController
from app.settings import ALLOWED_HOSTS
from front.views import Redirector

@pytest.mark.django_db
class TestClient(TestCase):

    def setUp(self):
        # реализация fakeredis используется для сокращения времени тестирования - позволяет не разворачивать лишние контейнеры
        file = open('common/fixtures/dummy_urls.json', 'r')
        self.test_urls = json.load(file)
        server = fakeredis.FakeServer()
        fake_redis = fakeredis.FakeStrictRedis(server=server)
        self._url_controller = UrlsController(fake_redis)

    def test_not_allowed_host(self):
        not_allowed_host = f'https://{ALLOWED_HOSTS[0]}/some_way'
        logger.info(f'Test - not allowed host - {not_allowed_host}')
        self.assertRaises(ValidationError, self._url_controller.get_short_url, not_allowed_host)

    def test_list_of_urls(self):
        with self.assertRaises(ValidationError):
            logger.info('Testing list of data with broken 4\'th and 5\'th urls')
            short_urls = []
            for item in self.test_urls['urls']:
                short_urls.append(self._url_controller.get_short_url(item))
                
    def test_regular_work(self):
        logger.info('Testing normal user story')
        long_url = 'https://vk.com/individiumi/'
        short_url = self._url_controller.get_short_url(long_url)
        returned_long_url = self._url_controller.get_full_url(short_url)

        assert long_url == returned_long_url.decode("utf-8") 

    def test_schemas_validation(self):
        logger.info('Testing not url with not valid scheme')
        long_url = 'vk.com/individiumi/'
        with self.assertRaises(ValidationError):
            self._url_controller.get_short_url(long_url)
 