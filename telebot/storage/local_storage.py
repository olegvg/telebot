# -*- coding: utf-8 -*-

import functools
import ujson
from ..utils import AbstractSingletonMeta
from . import StorageMixin


# noinspection PyAbstractClass
class _Storage(StorageMixin):
    __metaclass__ = AbstractSingletonMeta
    __slots__ = ('_storage', '_prefix')

    def __init__(self, prefix):
        """
        Initializer of dict()-based storage singleton

        :param prefix: prefix for keys. Actually it doesn't need because of singleton nature of _Storage
        """
        self._prefix = unicode(prefix)
        self._storage = {}

    def get_by_key(self, key, default=None):
        key = self._prefix + unicode(key)
        jsn_value = self._storage.get(key, default)
        if jsn_value is default:
            return default
        return ujson.loads(jsn_value)

    def set_by_key(self, key, value):
        key = self._prefix + unicode(key)
        json_value = ujson.dumps(value, ensure_ascii=False)
        self._storage[key] = json_value

    def del_by_key(self, key):
        key = self._prefix + unicode(key)
        del self._storage[key]

    def is_key_exists(self, key):
        key = self._prefix + unicode(key)
        return key in self._storage

    def clear(self):
        """
            Clear of storage.
            Realized in redundant manner because there is no need in taking 'prefix' into account
        """
        for k in filter(lambda x: x.startswith(self._prefix), self._storage):
            del self._storage[k]

EphemeralStorage = functools.partial(_Storage, prefix='ephemeral:')
PersistentStorage = functools.partial(_Storage, prefix='persistent:')
