import connexion
from connexion import NoContent
from passlib.hash import pbkdf2_sha256
from flask import session
import orm
from decorators import access_checks

db_session = orm.init_db('postgresql://pybossa:tester@localhost/cccs')

def get_users(limit, search_term=None):
    q = db_session.query(orm.User)
    if search_term:
        q = q.filter(orm.User.username == search_term)
    return [q.dump() for u in q][:limit]

@access_checks.ensure_key
def get(user_id):
    user = db_session.query(orm.User).filter(orm.User.user_id == user_id).one_or_none()
    return user.dump() if user is not None else ('Not found', 404)

def register(user):
    logging.info('Creating user ')
    user['user_id'] = uuid.uuid4()
    user['api_key'] = uuid.uuid4()
    user['pwd'] = pbkdf2_sha256.encrypt(user['pwd'], rounds=200000, salt_size=16)
    project['created_at'] = datetime.datetime.utcnow()
    print(user)
    db_session.add(orm.User(**user))
    db_session.commit()
    return user.dump(), 201

def login(user):
    q = db_session.query(orm.User).filter(orm.User.user_id == user.user_id).one_or_none()
    if q:
        if pbkdf2_sha256.verify(user['pwd'], q['pwd']):
            session['user'] = q
            return q.dump(), 200
        else:
            return NoContent, 401
    else:
        return NoContent, 404

def logout():
    session['user'] = None
    del session['user']
    return 200