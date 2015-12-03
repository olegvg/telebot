# -*- coding: utf-8 -*-

from tornado import ioloop
from telebot import bot_servant


if __name__ == '__main__':
    main_loop = ioloop.IOLoop.instance()
    main_loop.run_sync(bot_servant)
