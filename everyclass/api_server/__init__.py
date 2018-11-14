import copy
import sys

import logbook
from elasticapm.contrib.flask import ElasticAPM
from flask import Flask
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
    from everyclass.api_server.v1 import blueprint as api_v1

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

    app.register_blueprint(api_v1)

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
