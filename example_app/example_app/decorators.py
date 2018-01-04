from functools import wraps
from flask import g, request, redirect, url_for
from example_app import app


def access_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.cookies.get('access_token')
        if access_token is None:
            return redirect(url_for('credentials', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
