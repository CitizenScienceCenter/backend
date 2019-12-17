from db import Media
from minio import PostPolicy
from flask import current_app
from datetime import datetime, timedelta

def get_for_source(id=None):
    m = Media.get(source_id=id)
    if m is not None:
        return m

def get_pre_signed_url(source_id, filename):
    post_policy = PostPolicy()
    post_policy.set_bucket_name(source_id)
    post_policy.set_key_startswith(filename)
    post_policy.set_content_length_range(10, 1024)
    expires_date = datetime.utcnow() + timedelta(days=10)
    post_policy.set_expires(expires_date)
    # Load client
    current_app.app.uploader.presigned_post_policy(post_policy)

    pass
