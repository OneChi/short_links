import json
import pytest

from django.test import TestCase

@pytest.mark.django_db
# @override_settings(SENSITIVE_DB_CONN=FAKE_REDIS_CONN)
class TestClient(TestCase):

    def setUp(self):
        self.test_urls = open('common/fixtures/dummy_urls.json', 'r').read()
        print(self.test_urls)

    def test_url_validator(self):
        print("test")
        assert 1 == 1
