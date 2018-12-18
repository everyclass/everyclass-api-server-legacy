# -*- coding: UTF-8 -*-
import pymongo
import pymysql
from DBUtils.PooledDB import PooledDB

from everyclass.api_server.config import get_config

"""
数据库连接与连接池的封装
"""


def mysql_connect():
    """
    建立单个MySQL数据库的连接
    :return: MySQL连接句柄
    """
    config = get_config()
    conn = pymysql.connect(**config['MYSQL_CONFIG'])
    conn.autocommit(1)  # 定义数据库不自动提交
    return conn


def mysql_pool():
    """
    通过配置参数建立链接并生成连接池
    :return: MySQl连接池
    """
    config = get_config()
    pool = PooledDB(creator=pymysql,
                    **getattr(config, 'MYSQL_CONFIG'),
                    **getattr(config, 'MYSQL_POOL_CONFIG'))  # 建立MySQL连接池
    return pool


def mongo_pool():
    """
    通过配置参数建立链接并生成连接池
    :return:
    """
    config = get_config()
    pool = pymongo.MongoClient(**getattr(config, 'MONGODB_CONN')
                               )[config['MONGODB_DB']]
    return pool
