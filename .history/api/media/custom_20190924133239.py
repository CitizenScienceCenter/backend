from db import Media
from app import uploader

def get_for_source(id=None):
    m = Media.get(source_id=id)
    if m is not None:
        return m

def get_pre_signed_url(filename):
    pass
