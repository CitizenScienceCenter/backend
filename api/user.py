import connexion
from connexion import NoContent

import orm

db_session = orm.init_db('postgresql://pybossa:tester@localhost/cccs')

def get_users(limit, search_term=None):
    q = db_session.query(orm.User)
    if search_term:
        q = q.filter(orm.User.username == search_term)
    return [q.dump() for u in q][:limit]

def get_user(user_id):
    user = db_session.query(orm.User).filter(orm.User.user_id == user_id).one_or_none()
    return user.dump() if user is not None else ('Not found', 404)

def register_user(user):
    logging.info('Creating user ')
    user['user_id'] = uuid.uuid4()
    user['api_key'] = uuid.uuid4()
    project['created_at'] = datetime.datetime.utcnow()
    print(user)
    db_session.add(orm.User(**user))
    db_session.commit()
    return NoContent, 201
