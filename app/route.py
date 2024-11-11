from app import app, mysql
from flask import Blueprint, render_template, flash, redirect, url_for, session
from functools import wraps
from app.decorators import login_required



main_bp = Blueprint('main',__name__)

@main_bp.route("/")
def index():
    session["temp"] = None
    return render_template("index.html")

@main_bp.route("/logout")
def logout():
    session["logged_in"] = False
    session["type"] = "None"
    session.clear()
    return redirect(url_for("main.index"))

@main_bp.route("/<string:username>/settings/account")
@login_required
def settings(username):
    if session["username"] == username:
        return render_template("/settings/account.html")
    else:
        flash("You can't access this page...", "danger")
        return redirect(url_for("main.index"))

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    s = "SELECT * FROM articles WHERE author = %s"
    result = cursor.execute(s, (session["username"],))
    if result > 0:
        articles = cursor.fetchall()
        return render_template("dashboard.html", articles=articles)
    else:
        return render_template("dashboard.html")
