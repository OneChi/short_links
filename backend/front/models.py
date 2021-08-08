from django.db import models
from django.core import validators
from app.settings import REDIS_PORT, REDIS_HOST, COUNTER_KEY, COUNTER_MAX_VALUE
import logging
import redis
import hashids
# Create your models here.
logger = logging.getLogger(__name__)


class UrlsStorage(models.Model):
    """Class for storing URLs"""

    key = models.BigIntegerField(null=False, blank=False)
    url_full = models.URLField(max_length=500)
    url_short = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deletable = models.BooleanField(default=True)


class UrlsController:

    def __init__(self, *args, **kwargs):
        self._redis = redis.Redis(REDIS_HOST, REDIS_PORT)
        self._hashids = hashids.Hashids()
        
    def _get_by_key(self, key: str) -> str:
        return self._redis.get(key)

    def _save_by_key(self, key: str, value: str) -> bool:
        return self._redis.set(key, value)

    def _get_next_counter(self) -> int:
        counter_value = self._redis.incr(COUNTER_KEY)
        if counter_value >= 10:
            self._redis.set(COUNTER_KEY, 0)
        print(counter_value)
        return counter_value


    # TODO проверка на уникальность, валидация, удаление старых
    def get_short_url(self, long_url: str) -> str:
        short_url = self._get_by_key(long_url) # искать это в базе а не в редисе
        if short_url is None:
            new_counter = self._get_next_counter()
            short_url = self._hashids.encode(new_counter)
            UrlsStorage.objects.create(key=new_counter, url_full=long_url, url_short=short_url)
            self._save_by_key(short_url, long_url)
        else: 
            return None
        return short_url

    def get_full_url(self, short_url: str) -> str:
        return self._get_by_key(short_url)
        