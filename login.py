from flask import session

# In-memory user store (use a database in production)
users = {}

def register_user(username, password):
    if username in users:
        return False
    users[username] = password
    return True

def login_user(username, password):
    return users.get(username) == password

def logout_user():
    session.pop('username', None)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function