import uuid
from datetime import datetime
from pony.orm import Set, PrimaryKey, Optional, Required, Json, Database, commit
from db.models import DB, Role

from pony.flask import db_session

default_roles = [
    {
        "name": "admin",
        "view_project": True,
        "edit_project": True,
        "delete_project": False,
        "view_tasks": True,
        "edit_tasks": True,
        "add_tasks": True,
        "delete_tasks": True,
        "edit_media": True,
        "delete_media": True,
        "view_submissions": True,
        "edit_submissions": True,
        "delete_submissions": False,
        "export_data": True,
    },
    {
        "name": "su",
        "view_project": True,
        "edit_project": True,
        "delete_project": True,
        "view_tasks": True,
        "edit_tasks": True,
        "add_tasks": True,
        "delete_tasks": True,
        "edit_media": True,
        "delete_media": True,
        "view_submissions": True,
        "edit_submissions": True,
        "delete_submissions": True,
        "export_data": True,
        "su": True,
    },
    {
        "name": "owner",
        "view_project": True,
        "edit_project": True,
        "delete_project": True,
        "view_tasks": True,
        "edit_tasks": True,
        "add_tasks": True,
        "delete_tasks": True,
        "edit_media": True,
        "delete_media": True,
        "view_submissions": True,
        "edit_submissions": True,
        "delete_submissions": True,
        "export_data": True,
    },
    {
        "name": "viewer",
        "view_project": True,
        "edit_project": False,
        "delete_project": False,
        "view_tasks": True,
        "edit_tasks": False,
        "add_tasks": True,
        "delete_tasks": False,
        "edit_media": False,
        "delete_media": False,
        "view_submissions": True,
        "edit_submissions": False,
        "delete_submissions": False,
        "export_data": True,
    }
]


class RoleHandler:
    def __init__(self, db):
        self.db = db

    @db_session
    def init_roles(self):
        for r in default_roles:
            existing = Role.get(name=r['name'])
            if existing:
                for k in r.keys():
                    setattr(existing, k, r[k])
            else:
                a = Role(**r)
                try:
                    commit()
                except Exception as e:
                    print(e)
