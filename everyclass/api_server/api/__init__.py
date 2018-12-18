# -*- coding: UTF-8 -*-
from flask import Blueprint

blueprint = Blueprint('api', __name__)

from .klass import hello_klass, get_klass_schedule
from .room import hello_room, get_room_schedule
from .search import hello_search, get_search
from .student import hello_student, get_student_schedule
from .teacher import hello_teacher, get_teacher_schedule
