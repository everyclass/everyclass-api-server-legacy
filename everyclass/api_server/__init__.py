import copy
import sys

import logbook
from elasticapm.contrib.flask import ElasticAPM
from flask import Flask
from flask_restplus import Api, Resource
from raven.contrib.flask import Sentry
from raven.handlers.logbook import SentryHandler

logger = logbook.Logger(__name__)

sentry = Sentry()


def create_app(offline=False) -> Flask:
    """创建 flask app
    @param offline: 如果设置为 `True`，则为离线模式。此模式下不会连接到 Sentry 和 ElasticAPM
    """
    from everyclass.utils.logbook_logstash.handler import LogstashHandler
    from everyclass.utils.logbook_logstash.formatter import LOG_FORMAT_STRING

    app = Flask(__name__)

    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in'  : 'header',
            'name': 'X-API-KEY'
        }
    }

    api = Api(app, version='1.0', title='EveryClass API',
              description='EveryClass API is currently in beta. We may change the API at any time.',
              authorizations=authorizations,
              security='apikey',
              doc='/doc/'
              )

    student_ns = api.namespace('student', description='学生相关')
    teacher_ns = api.namespace('teacher', description='老师相关')
    classroom_ns = api.namespace('classroom', description='教室相关')
    course_ns = api.namespace('course', description='课程相关')

    # load app config
    from everyclass.api_server.config import get_config
    _config = get_config()
    app.config.from_object(_config)

    """
    每课统一日志机制


    规则如下：
    - WARNING 以下 log 输出到 stdout
    - WARNING 以上输出到 stderr
    - DEBUG 以上日志以 json 形式通过 TCP 输出到 Logstash，然后发送到日志中心
    - WARNING 以上级别的输出到 Sentry


    日志等级：
    critical – for errors that lead to termination
    error – for errors that occur, but are handled
    warning – for exceptional circumstances that might not be errors
    notice – for non-error messages you usually want to see
    info – for messages you usually don’t want to see
    debug – for debug messages
    
    
    Sentry：
    https://docs.sentry.io/clients/python/api/#raven.Client.captureMessage
    - stack 默认是 False
    
    """
    stdout_handler = logbook.StreamHandler(stream=sys.stdout, bubble=True, filter=lambda r, h: r.level < 13)
    stdout_handler.format_string = LOG_FORMAT_STRING
    logger.handlers.append(stdout_handler)

    stderr_handler = logbook.StreamHandler(stream=sys.stderr, bubble=True, level='WARNING')
    stderr_handler.format_string = LOG_FORMAT_STRING
    logger.handlers.append(stderr_handler)

    if not offline and (app.config['CONFIG_NAME'] in ["production", "staging", "testing"]):
        # Sentry
        sentry.init_app(app=app)
        sentry_handler = SentryHandler(sentry.client, level='WARNING')  # Sentry 只处理 WARNING 以上的
        logger.handlers.append(sentry_handler)

        # Elastic APM
        ElasticAPM(app)

        # Log to Logstash
        logstash_handler = LogstashHandler(host=app.config['LOGSTASH']['HOST'],
                                           port=app.config['LOGSTASH']['PORT'],
                                           release=app.config['GIT_DESCRIBE'],
                                           logger=logger)
        logger.handlers.append(logstash_handler)

    @student_ns.route('/<string:student_id>/schedule/<string:semester>')
    @api.doc(params={'student_id': '学生 ID',
                     'semester'  : '学期，格式为 2018-2019-1'})
    class StudentSchedule(Resource):
        def get(self, student_id, semester):
            """
            获取学生在指定学期的课表
            """
            return {'hello': id}, 200

    @teacher_ns.route('/<string:teacher_id>/schedule/<string:semester>')
    @api.doc(params={'teacher_id': '教师 ID',
                     'semester'  : '学期，格式为 2018-2019-1'})
    class TeacherSchedule(Resource):
        def get(self, teacher_id, semester):
            """
            获取老师在指定学期的课表
            """
            return {'res': teacher_id,
                    'sem': semester}

    @classroom_ns.route('/<string:classroom_id>/<string:semester>')
    @api.doc(params={'classroom_id': '教室 ID',
                     'semester'    : '学期，格式为 2018-2019-1'})
    class Classroom(Resource):
        def get(self, classroom_id, semester):
            """
            获取教室活动
            """
            return {'res': classroom_id,
                    'sem': semester}

    @course_ns.route('/<string:course_id>/<string:semester>')
    @api.doc(params={'course_id': '课程 ID',
                     'semester' : '学期，格式为 2018-2019-1'})
    class Course(Resource):
        def get(self, course_id, semester):
            """
            获取一门课程的详情
            """
            return {'res': course_id,
                    'sem': semester}

    logger.info('App created with `{0}` config'.format(app.config['CONFIG_NAME']), stack=False)

    # 输出配置内容
    logger.info('Below are configurations we are using:')
    logger.info('================================================================')
    for key, value in app.config.items():
        if key not in ('SECRET_KEY',):
            value = copy.copy(value)

            # 敏感内容抹去
            if key == 'SENTRY_CONFIG':
                value['dsn'] = '[secret]'
            if key == 'MYSQL_CONFIG':
                value['password'] = '[secret]'
            if key == 'ELASTIC_APM':
                value['SECRET_TOKEN'] = '[secret]'

            logger.info('{}: {}'.format(key, value))
    logger.info('================================================================')

    return app
