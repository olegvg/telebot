# -*- coding: utf-8 -*-

from tornado import gen
from . import text_plugin_entry_point, TextPluginMixin, text_plugin_blueprints


@text_plugin_entry_point(u'/start')
class Start(TextPluginMixin):
    __help_enabled__ = False

    @staticmethod
    @gen.coroutine
    def first_entry_point(bot, message, *_):
        greet_message = u'This is stub greet message of Telebot bot framework.'

        yield bot.send_message(
            message.chat.id_,
            greet_message,
            reply_to_message_id=message.message_id
        )

    @staticmethod
    @gen.coroutine
    def subsequent_entry_point(*_):
        pass
