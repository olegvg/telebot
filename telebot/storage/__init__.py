# -*- coding: utf-8 -*-

import abc
import logging
from telebot import config, utils

logger = logging.getLogger('storage')


class StorageMixin(object):
    __metaclass__ = utils.AbstractSingletonMeta

    @abc.abstractmethod
    def get_by_key(self, key, default=None):
        pass

    @abc.abstractmethod
    def set_by_key(self, key, value):
        pass

    @abc.abstractmethod
    def del_by_key(self, key):
        pass

    @abc.abstractmethod
    def is_key_exists(self, key):
        pass

    @abc.abstractmethod
    def clear(self):
        pass


class StorageStub(object):
    def get_by_key(self, key, default=None):
        raise NotImplementedError

    def set_by_key(self, key, value):
        raise NotImplementedError

    def del_by_key(self, key):
        raise NotImplementedError

    def is_key_exists(self, key):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


def register_storage():
    ephemeral_storage_plugin = config.get_config(
        lambda x: x['telebot']['ephemeral_storage_plugin'],
        'local_storage'
    )

    persistent_storage_plugin = config.get_config(
        lambda x: x['telebot']['persistent_storage_plugin'],
        'local_storage'
    )

    global EphemeralStorage, PersistentStorage

    logger.debug("Storage plugin '{}' is going to be registered as ephemeral".format(ephemeral_storage_plugin))
    _ephemeral_module = __import__(ephemeral_storage_plugin, globals(), locals(), [], -1)
    EphemeralStorage = _ephemeral_module.EphemeralStorage

    logger.debug("Storage plugin '{}' is going to be registered as persistent".format(persistent_storage_plugin))
    _persistent_module = __import__(persistent_storage_plugin, globals(), locals(), [], -1)
    PersistentStorage = _persistent_module.PersistentStorage


EphemeralStorage = StorageStub()
PersistentStorage = StorageStub()
