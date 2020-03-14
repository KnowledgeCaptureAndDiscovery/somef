from flask import Blueprint

bp = Blueprint('git_class', __name__)

from app.giturl_class import routes
