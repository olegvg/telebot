# -*- coding: utf-8 -*-

import logging
import config


def init_root_logger():
    default_formatter = '%(asctime)s %(levelname)-8s %(name)-16s %(message)s'

    default_handler = logging.StreamHandler()
    default_formatter = logging.Formatter(default_formatter)
    default_handler.setFormatter(default_formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(default_handler)
    root_logger.setLevel(logging.DEBUG)

    root_log_format = config.get_config(
        lambda x: x['telebot']['logger']['root']['format'],
        default=default_formatter)
    root_log_level = config.get_config(
        lambda x: x['telebot']['logger']['root']['level'],
        default=logging.DEBUG
    )

    root_handler = logging.StreamHandler()
    root_formatter = logging.Formatter(root_log_format)
    root_handler.setFormatter(root_formatter)
    root_logger.removeHandler(default_handler)
    root_logger.addHandler(root_handler)
    root_logger.setLevel(root_log_level)

    tornado_log_format = config.get_config(
        lambda x: x['telebot']['logger']['tornado']['format'],
        default=default_formatter)
    tornado_log_level = config.get_config(
        lambda x: x['telebot']['logger']['tornado']['level'],
        default=logging.DEBUG
    )

    tornado_logger = logging.getLogger('tornado')
    tornado_handler = logging.StreamHandler()
    tornado_formatter = logging.Formatter(tornado_log_format)
    tornado_handler.setFormatter(tornado_formatter)
    tornado_logger.addHandler(tornado_handler)
    tornado_logger.setLevel(tornado_log_level)
