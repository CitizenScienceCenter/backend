from db import Media
from app import uploader
from minio import PostPolicy

def get_for_source(id=None):
    m = Media.get(source_id=id)
    if m is not None:
        return m

def get_pre_signed_url(source_id, filename):
    post_policy = PostPolicy()
    post_policy.set_bucket_name('my-bucketname')
    post_policy.set_key_startswith('my-objectname')
    post_policy.set_content_length_range(10, 1024)
    expires_date = datetime.utcnow()+timedelta(days=10)
    post_policy.set_expires(expires_date)

    pass
