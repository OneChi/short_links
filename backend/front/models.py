from django.db import models

from app.settings import REDIS_PORT, REDIS_HOST, COUNTER_KEY, COUNTER_MAX_VALUE

import redis
import hashids

# Create your models here.


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

    def _get_by_key(self, key: str) -> str:
        return self._redis.get(key)

    def _save_by_key(self, key: str, value: str) -> bool:
        return self._redis.set(key, value)

    
    def get_short_link(self, long_url: str) -> str:
        pass


    def post(self, request):
        pass

    def get(self, request):
        pass
