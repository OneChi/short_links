# type: ignore

from __future__ import absolute_import, unicode_literals

import json
import logging
from http import client as httplib
from app.settings import REDIS_PORT, REDIS_HOST
import redis
import datetime

from front.models import UrlsStorage
from celery import shared_task
from django.conf import settings
from app.celery import app

logger = logging.getLogger(__name__)


# TODO: удалять ли из основной базы?
# TODO: выгружать ли данные из базы в дамп
@app.task(bind=True)
def clear_outdated_urls(self, redis_server=None):
    logger.info("Clear outdated")
    if redis_server is None:
        redis_server = redis.Redis(REDIS_HOST, REDIS_PORT)
    outdated_date = datetime.datetime.now() - datetime.timedelta(days=1)
    data = UrlsStorage.objects.filter(created_at__lte=outdated_date)
    for item in data:
        logger.info(f'Delete url - {item.url_full}')
        redis_server.delete(item.url_short)


@app.task(bind=True)
def clear_all(self, redis_server=None):
    logger.info("Clear all redis")
    if redis_server is None:
        redis_server = redis.Redis(REDIS_HOST, REDIS_PORT)
    for item in redis_server.keys():
        redis_server.delete(item)
