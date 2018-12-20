import gc
import sys

import logbook
from flask import Flask
from raven.contrib.flask import Sentry
from raven.handlers.logbook import SentryHandler

logger = logbook.Logger(__name__)
sentry = Sentry()
__app = None
__first_spawn = True
__sentry_available = False

try:
    import uwsgidecorators

    """
    below are functions that will be executed in **each** process after fork().
    these functions will be executed in the same order of definition here.
    """

    @uwsgidecorators.postfork
    def enable_gc():
        """enable garbage collection"""
        gc.set_threshold(700)

    @uwsgidecorators.postfork
    def init_db():
        """init database connection"""
        import everyclass.api_server.util
        global __app
        __app.mysql_pool = everyclass.api_server.util.mysql_pool()
        __app.mongo_pool = everyclass.api_server.util.mongo_pool()

    @uwsgidecorators.postfork
    def init_log_handlers():
        """init log handlers"""
        from everyclass.api_server.util.logbook_logstash.handler import LogstashHandler
        from elasticapm.contrib.flask import ElasticAPM
        from everyclass.api_server.util import monkey_patch
        ElasticAPM.request_finished = monkey_patch.ElasticAPM.request_finished(ElasticAPM.request_finished)

        global __app, __first_spawn, __sentry_available

        # Sentry
        if __app.config['CONFIG_NAME'] in __app.config['SENTRY_AVAILABLE_IN']:
            sentry.init_app(app=__app)
            sentry_handler = SentryHandler(sentry.client, level='WARNING')  # Sentry 只处理 WARNING 以上的
            logger.handlers.append(sentry_handler)
            __sentry_available = True
            logger.info('You are in {} mode, so Sentry is inited.'.format(__app.config['CONFIG_NAME']))

        # Elastic APM
        if __app.config['CONFIG_NAME'] in __app.config['APM_AVAILABLE_IN']:
            ElasticAPM(__app)
            logger.info('You are in {} mode, so APM is inited.'.format(__app.config['CONFIG_NAME']))

        # Logstash centralized log
        if __app.config['CONFIG_NAME'] in __app.config['LOGSTASH_AVAILABLE_IN']:
            logstash_handler = LogstashHandler(host=__app.config['LOGSTASH']['HOST'],
                                               port=__app.config['LOGSTASH']['PORT'],
                                               release=__app.config['GIT_DESCRIBE'],
                                               bubble=True,
                                               logger=logger,
                                               filter=lambda r, h: r.level >= 11)  # do not send DEBUG
            logger.handlers.append(logstash_handler)
            logger.info('You are in {} mode, so LogstashHandler is inited.'.format(__app.config['CONFIG_NAME']))

        import uwsgi
        if uwsgi.worker_id() == 1 and __first_spawn:
            from everyclass.api_server.util import mysql_connect, get_semester_list

            logger.info('数据库可用学期：' + ';'.join(get_semester_list(__app.mongo_pool)))

            __first_spawn = False
except ModuleNotFoundError:
    print('ModuleNotFound when importing uWSGI-decorators. Ignore this if you are not launched from uWSGI.')


def create_app(outside_container=False) -> Flask:
    """创建 flask app
    @param outside_container: 是否不在容器内运行
    """
    import os
    from flask import jsonify

    from everyclass.api_server.util.logbook_logstash.formatter import LOG_FORMAT_STRING
    from everyclass.api_server.util import mysql_pool, mongo_pool
    from everyclass.api_server.api import blueprint as api_v1_blueprint

    app = Flask(__name__)

    # load app config
    from everyclass.api_server.config import get_config
    _config = get_config()
    app.config.from_object(_config)

    app.register_blueprint(api_v1_blueprint, url_prefix='/v1')

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

    # 容器外运行（无 uWSGI）时初始化数据库
    if outside_container and (os.environ.get("MODE") == 'DEVELOPMENT'):
        app.mysql_pool = mysql_pool()
        app.mongo_pool = mongo_pool()

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    # 查询的资源不存在
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'message': str(error)}), 404

    # 访问参数异常处理
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'message': str(error)}), 400

    # 访问参数异常处理
    @app.errorhandler(500)
    def server_internal_error(error):
        return jsonify({'message': str(error)}), 500

    global __app
    __app = app

    return app
