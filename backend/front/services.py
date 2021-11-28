from asyncio import sleep
from app.settings import REDIS_PORT, REDIS_HOST, COUNTER_KEY
import logging
import redis
import hashids
from .models import UrlsStorage

URL_COUNTER_MAX_VALUE = 2000000

logger = logging.getLogger(__name__)


class UrlsController:

    def __init__(self, *args, **kwargs):
        self._redis = redis.Redis(REDIS_HOST, REDIS_PORT)
        self._hashids = hashids.Hashids()

    def _keys(self):
        return self._redis.keys()

    def _get_by_key(self, key: str) -> str:
        return self._redis.get(key)

    def _save_by_key(self, key: str, value: str) -> bool:
        return self._redis.set(key, value)

    def _get_next_counter(self) -> int:
        counter_value = self._redis.incr(COUNTER_KEY)
        if counter_value >= URL_COUNTER_MAX_VALUE:
            self._redis.set(COUNTER_KEY, 0)
        logger.warning(counter_value)
        return counter_value

    async def _increment_redirect_counter(self, long_url, short_url) -> int:
        instance = UrlsStorage.objects.filter(url_full=long_url, url_short=short_url)
        instance.counter = instance.counter + 1
        instance.save()
        logger.warning(f'Requestred {long_url} - {instance.counter} times')

    def get_short_url(self, long_url: str) -> str:
        # как вариант, чтобы обезопасить себя от потери данных в редисе - искать это в базе а не в редисе
        short_url = self._get_by_key(long_url)
        if short_url is None:
            new_counter = self._get_next_counter()
            short_url = self._hashids.encode(new_counter)
            UrlsStorage.objects.create(key=new_counter, url_full=long_url, url_short=short_url)
            self._save_by_key(short_url, long_url)
            logger.warning(f"saved - {long_url} - to - {short_url}")
        return short_url

    def get_full_url(self, short_url: str) -> str:
        long_url = self._get_by_key(short_url)
        # await self._increment_redirect_counter(long_url, short_url)
        return long_url
