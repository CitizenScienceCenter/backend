from db import User

def get_user(request, db):
    key = request.headers['X-API-KEY']
    return db.query(User).filter(User.api_key == key).one_or_none()