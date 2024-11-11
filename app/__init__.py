from flask import Flask
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__,)
app.config.from_object(Config)
app.secret_key = "bkk"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "educationBlog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

from app.routes import student, teacher, article, questions, password, admin

def register_blueprints(app):
    from app.routes.student import student_bp
    from app.routes.teacher import teacher_bp
    from app.routes.article import article_bp
    from app.routes.questions import question_bp
    from app.routes.password import password_bp
    from app.routes.admin import admin_bp
    from app.route import main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(student_bp, url_prefix='/')
    app.register_blueprint(teacher_bp, url_prefix='/')
    app.register_blueprint(article_bp, url_prefix='/')
    app.register_blueprint(question_bp, url_prefix='/')
    app.register_blueprint(password_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/')

register_blueprints(app)
