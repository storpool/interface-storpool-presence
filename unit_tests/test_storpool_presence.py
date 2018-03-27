#!/usr/bin/python3

"""
A set of unit tests for the storpool-presence interface.
"""

import os
import sys
import unittest

import mock

root_path = os.path.realpath('.')
if root_path not in sys.path:
    sys.path.insert(0, root_path)

lib_path = os.path.realpath('unit_tests/lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

from spcharms import service_hook
from spcharms import utils as sputils

import provides as testee_provides
import requires as testee_requires


class TestStorPoolPresence(unittest.TestCase):
    def get_call_count(self, obj):
        """
        Fetch the current call count of the tools used.
        """
        return {
            'rdebug': sputils.rdebug.call_count,
            'handle': service_hook.handle_remote_presence.call_count,
            'remove': obj.remove_state.call_count,
        }

    def check_update_call_count(self, obj, ref, delta):
        """
        Fetch the current call count and check that the delta is
        the same as the expected one.
        """
        current = self.get_call_count(obj)
        for (k, v) in delta.items():
            ref[k] += v
        self.assertEqual(current, ref)

    def do_test(self, obj):
        """
        Test the data exchanged by the provides or requires interface.
        """
        obj = testee_provides.StorPoolPresenceProvides('storpool-presence:42')
        obj.remove_state = mock.Mock()
        call_c = self.get_call_count(obj)

        obj.changed()
        self.check_update_call_count(obj, call_c, {
            'rdebug': 1,
            'handle': 1,
        })

        obj.broken()
        self.check_update_call_count(obj, call_c, {
            'rdebug': 1,
            'remove': 1,
        })

    def test_provides(self):
        """
        Test the data exchanged by the provides interface.
        """
        obj = testee_provides.StorPoolPresenceProvides('storpool-presence:42')
        self.do_test(obj)

    def test_requires(self):
        """
        Test the data exchanged by the provides interface.
        """
        obj = testee_requires.StorPoolPresenceRequires('storpool-presence:42')
        self.do_test(obj)
