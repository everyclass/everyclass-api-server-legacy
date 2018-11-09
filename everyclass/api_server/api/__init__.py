"""
API related
"""
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)

from everyclass.api_server.api.v1 import get_courses, get_semesters, error_handler_403
