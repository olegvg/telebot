# -*- coding: utf-8 -*-

import abc
import logging
from telebot import config

text_plugin_blueprints = {}

logger = logging.getLogger('plugins')


class TextPluginMixin(object):
    __metaclass__ = abc.ABCMeta
    __help_string__ = u'No help string. Please add it.'
    __help_enabled__ = True

    # noinspection PyMethodParameters
    @abc.abstractmethod
    def first_entry_point(bot, message, match, session, persistent_data):
        """
        First plugin entry point. Must be @staticmethod

        Obligatory parameters of descendants:
        :param bot: telezombie.api.TeleLich() instance itself
        :param message: inbound telezombie.types.Message()
        :param match: re.MatchObject() instance
        :param session:  ephemeral session which actual during single _this_ query
        :param persistent_data: persistent data which actual forever
        :return: telezombie.types.Message() instance returning from bot.send_message()
        if it's waiting for further user input, None otherwise
        """
        pass

    # noinspection PyMethodParameters
    @abc.abstractmethod
    def subsequent_entry_point(bot, message, session, persistent_data):
        """
        Second and further plugin entry point. Must be @staticmethod

        Obligatory parameters of descendants:
        :param bot: telezombie.api.TeleLich() itself
        :param message: inbound telezombie.types.Message()
        :param session:  ephemeral session which actual during single _this_ query
        :param persistent_data: persistent data which actual forever
        :return: telezombie.types.Message() instance returning from bot.send_message()
        if it's waiting for further user input, None otherwise
        """
        pass


def text_plugin_entry_point(entry_regex, entry_name=None):
    def decorator(cls):
        if entry_name is None:
            class_name = cls.__name__
        else:
            class_name = entry_name
        if class_name in text_plugin_blueprints:
            logger.fatal("Plugin entry point with same name '{}' already exists".format(class_name))
            raise Exception
        logger.debug("Register a new plugin '{}'".format(class_name))

        text_plugin_blueprints[class_name] = [entry_regex, cls]
    return decorator


def register_plugins():
    plugins = config.get_config(
        lambda x: x['telebot']['plugins'],
        None
    )
    if not isinstance(plugins, list):
        return
    for plugin_module in plugins:
        logger.debug("Plugin '{}' is going to be registered".format(plugin_module))
        __import__(plugin_module, globals(), locals(), [], -1)
