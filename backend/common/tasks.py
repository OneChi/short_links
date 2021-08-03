# type: ignore

from __future__ import absolute_import, unicode_literals

import json
import logging
from http import client as httplib

from celery import shared_task
from django.conf import settings
from app.celery import app




@shared_task
def hello():
    print("Hello there!") 


@app.task(bind=True)
def delete_mediafile(self, filepath):
    default_storage.delete(filepath)
    logger.info(f'File deteled: {filepath}')
