# -*- coding: utf-8 -*-

import abc
import logging


class AbstractStatic(staticmethod):
    __slots__ = ()

    def __init__(self, function):
        super(AbstractStatic, self).__init__(function)
        function.__isabstractmethod__ = True
    __isabstractmethod__ = True


class AbstractSingletonMeta(abc.ABCMeta):
    # noinspection PyArgumentList
    def __call__(cls, *args, **kwargs):
        key = 'inst_' + str(hash(tuple(args + tuple(sorted(kwargs.items())))))
        if getattr(cls, key, None) is None:
            storage_logger = logging.getLogger('storage')
            storage_logger.debug('Create a new singleton {} with args: {}, {}'.format(cls.__name__, args, kwargs))
            new_inst = super(AbstractSingletonMeta, cls).__call__(*args, **kwargs)
            setattr(cls, key, new_inst)
        return getattr(cls, key)
