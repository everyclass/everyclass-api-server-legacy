# -*- coding: UTF-8 -*-
from flask import Blueprint

blueprint = Blueprint('api_v1', __name__)

from everyclass.api_server.api.klass import hello_klass, get_klass_schedule
from everyclass.api_server.api.room import hello_room, get_room_schedule
from everyclass.api_server.api.search import hello_search, get_search
from everyclass.api_server.api.student import hello_student, get_student_schedule
from everyclass.api_server.api.teacher import hello_teacher, get_teacher_schedule
