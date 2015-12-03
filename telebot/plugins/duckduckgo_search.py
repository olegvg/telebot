# -*- coding: utf-8 -*-

import logging
import urllib
from telezombie import types
from tornado import gen, httpclient
import ujson
from . import text_plugin_entry_point, TextPluginMixin

DUCKDUCKGO_SEARCH_API_ENDPOINT = 'http://api.duckduckgo.com/'

logger = logging.getLogger('plugins')


# @text_plugin_entry_point(u'(?:/г|г|/g|g)\s+?(.*)')
@text_plugin_entry_point(u'/d')
class SequencedDuckduckgoTextSearch(TextPluginMixin):
    __help_string__ = u'/d - search in DuckDuckGo'

    @staticmethod
    @gen.coroutine
    def first_entry_point(bot, message, match, *_):
        try:
            res = yield bot.send_message(
                message.chat.id_,
                "duck wat?",
                reply_to_message_id=message.message_id,
                reply_markup=types.ForceReply(True)
            )
            raise gen.Return(res)
        except httpclient.HTTPError as e:
            logger.debug(str(e))

    @staticmethod
    @gen.coroutine
    def subsequent_entry_point(bot, message, *_):
        # google_res = google.search(message.text, 1, lang='ru')
        # if len(google_res) > 0 and google_res[0] is not None and google_res[0].link:
        #     link = google_res[0].link
        # else:
        #     link = "Don't know"

        query = message.text.strip(' ').encode('utf-8')
        params_dict = {
            'format': 'json',
            'q': query
        }
        params = urllib.urlencode(params_dict)
        url = DUCKDUCKGO_SEARCH_API_ENDPOINT + '?' + params

        httpc = httpclient.AsyncHTTPClient()
        try:
            resp = yield httpc.fetch(url)
            link = ujson.loads(resp.body)['AbstractURL']
            if link == u'':
                link = 'No results'
        except httpclient.HTTPError as e:
            logger.debug('DuckDuckGo plugin search error {} with query {}'.format(str(e), query))
            link = 'DuckDuckGo error'

        try:
            yield bot.send_message(
                message.chat.id_,
                link,
                reply_to_message_id=message.message_id
            )
        except httpclient.HTTPError as e:
            logger.debug(str(e))

        httpc.close()
        return


@text_plugin_entry_point(u'/d\s+?(.+)')
class DuckduckgoTextSearch(TextPluginMixin):
    __help_string__ = u'/d query - search in DuckDuckGo immediately'

    @staticmethod
    @gen.coroutine
    def first_entry_point(bot, message, match, *_):
        query = match.group(1).encode('utf-8')
        params_dict = {
            'format': 'json',
            'q': query
        }
        params = urllib.urlencode(params_dict)
        url = DUCKDUCKGO_SEARCH_API_ENDPOINT + '?' + params

        httpc = httpclient.AsyncHTTPClient()
        try:
            resp = yield httpc.fetch(url)
            link = ujson.loads(resp.body)['AbstractURL']
            if link == u'':
                link = 'No results'
        except httpclient.HTTPError as e:
            logger.debug('DuckDuckGo plugin search error {} with query {}'.format(str(e), query))
            link = 'DuckDuckGo error'

        try:
            yield bot.send_message(
                message.chat.id_,
                link,
                reply_to_message_id=message.message_id
            )
        except httpclient.HTTPError as e:
            logger.debug(str(e))

        httpc.close()
        return

    @staticmethod
    @gen.coroutine
    def subsequent_entry_point(bot, *_):
        pass
