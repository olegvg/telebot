# -*- coding: utf-8 -*-

import unittest
from telebot.storage import EphemeralStorage


class TestEphemeralSession(unittest.TestCase):
    def setUp(self):
        from telebot.logger import init_root_logger
        init_root_logger()


    def test_session_storage_singleton(self):
        session1 = EphemeralStorage()
        session1.set_by_key(1, 1)

        session2 = EphemeralStorage()
        session2.set_by_key(2, 2)

        self.assertEqual(session1, session2)

    def test_session_storage_cleanup(self):
        sess = EphemeralStorage()

        sess.set_by_key(1, 1)
        sess.set_by_key(2, 2)
        sess.set_by_key(3, 3)

        sess.clear()

        self.assertFalse(sess.is_key_exists(1))
        self.assertFalse(sess.is_key_exists(2))
        self.assertFalse(sess.is_key_exists(3))
