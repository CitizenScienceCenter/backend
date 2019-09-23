from minio import Minio

class Uploader():

    def __init__(self, url, access, secret, secure=True):
        self.client = Minio(url,
                            access_key=access,
                            secret_key=secret,
                            secure=secure)
