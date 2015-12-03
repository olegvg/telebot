# -*- coding: utf-8 -*-

import re

from tornado import gen

from telezombie import api, types

from plugins import text_plugin_blueprints
import storage


class TelegramBot(api.TeleLich):
    @gen.coroutine
    def on_text(self, message):
        ephemeral_storage = storage.EphemeralStorage()
        persistent_storage = storage.PersistentStorage()

        if message.reply_to_message is None:
            for plugin_name in text_plugin_blueprints:
                regex, cls = text_plugin_blueprints[plugin_name]
                match = re.match(regex, message.text)
                if match is not None:
                    break
            else:
                return

            session_key = '{}:{}'.format(message.chat.id_, message.from_.id_)
            # There is a potential race condition and it need to be wrapped by transaction or kinda compare-and-swap
            # operation but it is very rare and harmless condition and I fix it in future releases using context
            # manager
            if ephemeral_storage.is_key_exists(session_key):
                ephemeral_storage.del_by_key(session_key)

            session_dict = {}
            persistent_key = '{}:{}'.format(plugin_name, message.from_.id_)
            persistent_dict = persistent_storage.get_by_key(persistent_key, {})

            res = yield cls.first_entry_point(self, message, match, session_dict, persistent_dict)

            persistent_storage.set_by_key(persistent_key, persistent_dict)

            # Store ephemeral storage if plugin hasn't finished
            if isinstance(res, types.Message):
                ephemeral_storage.set_by_key(session_key, [plugin_name, session_dict])

        else:
            session_key = '{}:{}'.format(message.chat.id_, message.from_.id_)

            # There is a potential race condition and it need to be wrapped by transaction or kinda compare-and-swap
            # operation but it is very rare and harmless condition and I fix it in future releases using context
            # manager
            if not ephemeral_storage.is_key_exists(session_key):
                return

            plugin_name, session_dict = ephemeral_storage.get_by_key(session_key)

            persistent_key = '{}:{}'.format(plugin_name, message.from_.id_)
            persistent_dict = persistent_storage.get_by_key(persistent_key, {})

            _, cls = text_plugin_blueprints[plugin_name]
            res = yield cls.subsequent_entry_point(self, message, None, session_dict, persistent_dict)

            persistent_storage.set_by_key(persistent_key, persistent_dict)

            # Delete ephemeral storage if plugin has finished
            if not isinstance(res, types.Message):
                ephemeral_storage.del_by_key(session_key)
            else:
                ephemeral_storage.set_by_key(session_key, [plugin_name, session_dict])
