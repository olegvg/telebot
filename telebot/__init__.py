# -*- coding: utf-8 -*-

import logging
from tornado import gen, httpclient
from telebot import bot, config, logger, storage, plugins

logger.init_root_logger()
storage.register_storage()
plugins.register_plugins()

httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')


@gen.coroutine
def bot_servant():
    api_token = config.get_config(
        lambda x: x['telebot']['api_key']
    )

    if api_token is None:
        init_logger = logging.getLogger('telebot_init')
        init_logger.fatal('Telegram API token is not specified')
        raise Exception

    lich = bot.TelegramBot(api_token)

    yield lich.poll()
