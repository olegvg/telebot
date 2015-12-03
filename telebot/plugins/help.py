# -*- coding: utf-8 -*-

from tornado import gen
from . import text_plugin_entry_point, TextPluginMixin, text_plugin_blueprints


@text_plugin_entry_point(u'/help')
class Help(TextPluginMixin):
    __help_string__ = u'/help - show this message'
    __help_enabled__ = True

    @staticmethod
    @gen.coroutine
    def first_entry_point(bot, message, *_):
        help_strings = [x[1].__help_string__ for x in sorted(text_plugin_blueprints.values())
                        if x[1].__help_enabled__ is True]
        help_message = u"Bot commands:\n" + u'\n'.join(help_strings)

        yield bot.send_message(
            message.chat.id_,
            help_message,
            reply_to_message_id=message.message_id
        )

    @staticmethod
    @gen.coroutine
    def subsequent_entry_point(*_):
        pass
