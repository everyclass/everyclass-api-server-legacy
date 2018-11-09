import copy
import sys

import logbook
import logbook.queues
from elasticapm.contrib.flask import ElasticAPM
from flask import Flask, jsonify
from raven.contrib.flask import Sentry
from raven.handlers.logbook import SentryHandler

logger = logbook.Logger(__name__)

sentry = Sentry()


def create_app(offline=False) -> Flask:
    """创建 flask app
    @param offline: 如果设置为 `True`，则为离线模式。此模式下不会连接到 Sentry 和 ElasticAPM
    """
    from everyclass.api_server.db.dao import new_user_id_sequence
    from everyclass.api_server.db.mysql import get_connection, init_pool
    from everyclass.utils.log import LogstashHandler, LOG_FORMAT_STRING

    app = Flask(__name__)

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

    # 初始化数据库
    if not offline and (app.config['CONFIG_NAME'] in ("production", "staging", "testing", "development")):
        init_pool(app)

    # 导入并注册 blueprints
    from everyclass.api_server.views import main_blueprint as main_blueprint
    from everyclass.api_server.api import api_v1 as api_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    @app.errorhandler(500)
    def internal_server_error():
        return jsonify({'success': False,
                        'message': 'Server could not response to the request.'})

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
