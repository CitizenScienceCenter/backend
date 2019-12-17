import logging
from db import Media
from minio.error import ResponseError
from flask import current_app
from datetime import datetime, timedelta
from middleware.response_handler import ResponseHandler


def get_for_source(id=None):
    m = Media.get(source_id=id)
    if m is not None:
        return m


def get_pre_signed_url(source_id, filename):
    client = current_app.uploader

    try:
        if not client.bucket_exists(source_id):
            client.make_bucket(source_id)
    except ResponseError as e:
        logging.error(e)

    url = current_app.uploader.presigned_put_object(
        source_id, filename, expires=timedelta(days=3)
    )
    return ResponseHandler(200, {"url": url}).send()
