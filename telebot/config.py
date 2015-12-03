# -*- coding: utf-8 -*-

import sys
import linecache
import logging
import yaml

DEFAULT_CONFIG_FILE = './telebot_config.yml'

config_logger = logging.getLogger('config')

config = None


def config_loader():
    if len(sys.argv) == 2 and sys.argv[1].startswith('-') is not True:
        config_file = sys.argv[1]
    else:
        config_file = DEFAULT_CONFIG_FILE

    with open(config_file) as cfg_yml:
        return yaml.load(cfg_yml)


def get_config(fn, default=None):
    global config
    if config is None:
        config = config_loader()
    try:
        return fn(config)
    except (KeyError, TypeError) as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_traceback = exc_traceback.tb_next

        filename = exc_traceback.tb_frame.f_code.co_filename
        lineno = exc_traceback.tb_lineno
        line = linecache.getline(filename, lineno)
        err = "config option {} not found at {}:{}:{}".format(e, filename, lineno, line)

        config_logger.error(err)

        return default
