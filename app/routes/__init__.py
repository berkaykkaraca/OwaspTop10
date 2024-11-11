from flask import Blueprint

routes = Blueprint('routes', __name__)

from app.routes import student, teacher, article, questions, password, admin
from app import decorators,forms,route
