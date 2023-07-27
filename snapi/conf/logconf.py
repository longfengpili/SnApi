# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-17 18:04:38
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-27 13:44:15


import re
import os
import sys
import colorlog


# logging settings
USERPATH = os.environ['USERPROFILE'] if 'USERPROFILE' in os.environ else os.environ['HOME'] if 'HOME' in os.environ else ''
LOG_BASE_PATH = os.path.join(USERPATH, 'snapilog')  # 可以user目录下查看日志
PROJECT_NAME = re.sub(':?\\\\', '_', os.getcwd())
PROJECT_NAME = PROJECT_NAME[1:] if PROJECT_NAME.startswith('/') else PROJECT_NAME  # linux

LOGGING_CONFIG = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            'format': '%(asctime)s.%(msecs)03d - %(threadName)s:%(thread)d - %(name)s - %(levelname)s - %(pathname)s - %(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # 简单的日志格式
        'simple': {
            'format': '%(asctime)s.%(msecs)03d - %(threadName)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '%(message)s'
        },
        # color
        'color': {
            '()': colorlog.ColoredFormatter,
            'format': '%(asctime)s.%(msecs)03d - %(threadName)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(log_color)s%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'CRITICAL': 'bold_red',
                'ERROR': 'red',
                'WARNING': 'purple',
                'INFO': 'green',
                'DEBUG': 'yellow'
            }
        }
    },
    # 过滤器
    'filters': {
    },
    # 处理器
    'handlers': {
        # 在终端打印
        'console': {
            'level': 'DEBUG',
            'filters': [],
            'class': 'logging.StreamHandler',  #
            'formatter': 'color' if sys.stdout.isatty() else 'simple'
        },
        # 默认的
        'default': {
            'level': 'INFO',
            'class': 'snapi.conf.MakeFileHandler',  # 能够判断创建日持文件
            'filename': os.path.join(LOG_BASE_PATH, f'{PROJECT_NAME}_default.log'),  # 日志文件
            'when': 'd',  # 每天备份
            'interval': 1,
            'backupCount': 30,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'snrequests': {
            'level': 'INFO',
            'class': 'snapi.conf.MakeFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(LOG_BASE_PATH, f'{PROJECT_NAME}_snrequests.log'),  # 日志文件
            'when': 'd',  # 每小时备份
            'interval': 1,
            'backupCount': 30,
            'formatter': 'simple',
            'encoding': "utf-8"
        },
        'api': {
            'level': 'INFO',
            'class': 'snapi.conf.MakeFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(LOG_BASE_PATH, f'{PROJECT_NAME}_api.log'),  # 日志文件
            'when': 'd',  # 每小时备份
            'interval': 1,
            'backupCount': 30,
            'formatter': 'simple',
            'encoding': "utf-8"
        },
    },
    'loggers': {
        # 默认的logger应用如下配置
        '': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': True,  # 向不向更高级别的logger传递
        },
        'snapi.snrequests': {
            'handlers': ['console', 'snrequests'],
            'level': 'DEBUG',
            'propagate': False,  # 向不向更高级别的logger传递
        },
        'api': {
            'handlers': ['console', 'api'],
            'level': 'INFO',
            'propagate': False,  # 向不向更高级别的logger传递
        },
    },
}
