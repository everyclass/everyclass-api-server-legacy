from flask_restplus import Api

from .classroom import api as classroom_ns
from .course import api as course_ns
from .misc import api as misc_ns
from .student import api as student_ns
from .teacher import api as teacher_ns

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in'  : 'header',
        'name': 'X-API-KEY'
    },
    'oauth2': {
        'type'    : 'oauth2',
        'flow'    : 'accessCode',
        'tokenUrl': 'https://somewhere.com/token',
        'scopes'  : {
            'read' : 'Grant read-only access',
            'write': 'Grant read-write access',
        }
    }
}

api = Api(version='1.0', title='EveryClass API',
          description='EveryClass API is currently in beta. We may change the API at any time.',
          authorizations=authorizations,
          security='apikey',
          doc='/doc/'
          )

api.add_namespace(student_ns, path='/student')
api.add_namespace(teacher_ns, path='/teacher')
api.add_namespace(classroom_ns, path='/classroom')
api.add_namespace(course_ns, path='/course')
api.add_namespace(misc_ns, path='/')
