import connexion
from flask import abort, request
from pony.flask import db_session
from sqlalchemy.orm import joinedload, lazyload
from pony.orm import commit
from db import Project, Submission, Task, User, utils, Member, Role, ProjectGroup
from decorators import access_checks
from middleware.response_handler import ResponseHandler


@db_session
@access_checks.ensure_owner(Project)
def invite_member(pid, body):
    r = Role.get(name=body["role"])
    u = User.get(username=body["username"])
    p = Project.get(id=pid)
    if p and u and r:
        m = Member(user_id=u, project_id=p, role=r)
        try:
            commit()
            return ResponseHandler(200, "User added to project").send()
        except Exception as e:
            abort(500, e)
    else:
        abort(404, "User not found")

@db_session
@access_checks.ensure_owner(ProjectGroup)
def invite_member_group(gid, body):
    r = Role.get(name=body["role"])
    u = User.get(username=body["username"])
    p = ProjectGroup.get(id=gid)
    if p and u and r:
        m = Member(user_id=u, project_group_id=p, role=r)
        try:
            commit()
            return ResponseHandler(200, "User added to project group").send()
        except Exception as e:
            abort(500, e)
    else:
        abort(404, "User not found")
