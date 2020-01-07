from datetime import datetime
from pony import orm
from pony_up.do_update import Migrator


def do_update(migrator):
    assert isinstance(migrator, Migrator)
    print(migrator)
    print(str(migrator))
    assert migrator.new_db
    db = migrator.new_db
    db.execute('ALTER TABLE media add column task uuid;')
    db.execute('ALTER TABLE media add column submission uuid;')
    db.execute('ALTER TABLE media add column project uuid;')
    db.execute('ALTER TABLE projects add column anonymous_allowed bool;')
    db.execute('ALTER TABLE projects add column platform varchar;')
    db.execute('ALTER TABLE projects add column "group" uuid;')
    db.execute('ALTER TABLE oauth_tokens add column expiry timestamp;')
    db.execute('ALTER TABLE oauth_tokens add column token uuid;')
    db.execute('ALTER TABLE oauth_tokens add column owner uuid;')
    db.execute('ALTER TABLE users add column anonymous bool;')
    db.execute('ALTER TABLE submissions add column response jsonb;')
    db.execute('ALTER TABLE tasks add column part_of uuid;')
    return 12, {"message": "Added columns to media, projects, oauth_tokens, users, submissions and tasks."}