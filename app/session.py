from flask_restplus import abort
from models.session import SessionModel
from functools import wraps
from flask import request
from typing import Optional

def require_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'Token' in request.headers:
            token = request.headers["Token"]

            session: Optional[SessionModel] = SessionModel.query.filter_by(uuid=token).first()

            if session is None:
                abort(400, "invalid token")

            kwargs["session"] = session

            return f(*args, **kwargs)
        else:
            abort(400, "token required")

    return wrapper
