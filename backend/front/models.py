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
    # TODO можно сделать механизм TTL, теоретически - его можно хранить и в редисе