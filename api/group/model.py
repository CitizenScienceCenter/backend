import connexion
from connexion import NoContent
from db import orm_handler, Comment, utils, Group, User
from decorators import access_checks
from flask import request
import logging
from api import model

db_session = orm_handler.db_session


def get_groups(limit=20, search_term=None):
    return model.get_all(Group, limit, search_term)


def get_group(id=None):
    return model.get_one(Group, id)


@access_checks.ensure_key
def create_group(group):
    user = utils.get_user(request, db_session)
    group["owned_by"] = user.id
    g = Group(**group)
    user.member_of.append(g)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(g)
    return g.dump(), 201


@access_checks.ensure_key
def update_group(id, group):
    return model.put(Group, id, group)


@access_checks.ensure_owner(Group)
def delete_group(id):
    user = utils.get_user(request, db_session)
    group = db_session.query(Group).filter(Group.id==id).one_or_none()
    if group is None:
        return "Group was not found", 404
    users = db_session.query(User).filter(User.member_of.any(Group.id==group.id)).all()
    for u in users:
        u.member_of.remove(group)
    db_session.commit()
    return model.delete(Group, id)
