from functools import wraps
from flask import flash, redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Lütfen giriş yapınız...", "danger")
            return redirect(url_for("main.index"))
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["type"] == "teacher":
            return f(*args, **kwargs)
        else:
            flash("Please Login as a Teacher...", "danger")
            return redirect(url_for("main.index"))
    return decorated_function

def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["type"] == "admin":
            return f(*args, **kwargs)
        else:
            flash("Please Login as a Admin...", "danger")
            return redirect(url_for("main.index"))
    return decorated_function
