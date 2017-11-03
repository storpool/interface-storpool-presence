#!/usr/bin/python3

"""
A set of unit tests for the storpool-presence interface.
"""

import os
import platform
import sys
import testtools

import json
import mock

from charms import reactive

root_path = os.path.realpath('.')
if root_path not in sys.path:
    sys.path.insert(0, root_path)

lib_path = os.path.realpath('unit_tests/lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


import provides as testee_provides
import requires as testee_requires


class TestStorPoolPresence(testtools.TestCase):
    """
    Test the data exchanged by the storpool-presence interface.
    """
    @mock.patch('provides.StorPoolPresenceProvides.set_state')
    def test_provides(self, set_state):
        """
        Test that the provider interface sets a reactive state.
        """
        obj = testee_provides.StorPoolPresenceProvides('storpool-presence:42')
        obj.changed()
        set_state.assert_called_once_with('{relation_name}.notify')

        # That's all, folks!

    @mock.patch('requires.StorPoolPresenceRequires.set_state')
    @mock.patch('requires.StorPoolPresenceRequires.conversation')
    def test_requires(self, req_conv, set_state):
        """
        Test that the requires interface tries to exchange data.
        """
        sp_node = platform.node()

        obj = testee_requires.StorPoolPresenceRequires('storpool-presence:42')
        self.assertEquals(obj.sp_node, sp_node)

        def set_local_state(name, value):
            """
            Record all the invocations of conv.set_state() by the charm.
            """
            self.local_state.append((name, value))

        conv = mock.MagicMock(spec=reactive.relations.Conversation)
        conv.set_local.side_effect = set_local_state
        req_conv.return_value = conv

        self.loop_index = 0

        def check_something(supplied, expected, state_inc):
            """
            Invoke the "relationship changed" handler, passing the specified
            data as if it has arrived from the remote peer.
            """
            self.loop_index += 1
            conv.get_remote.return_value = supplied
            self.local_state = []
            state_count = set_state.call_count

            obj.changed()

            self.assertEquals(self.loop_index, conv.get_remote.call_count)
            self.assertEquals(self.loop_index, conv.set_local.call_count)
            self.assertEquals([('storpool_presence', expected)],
                              self.local_state)
            self.assertEquals(state_count + state_inc, set_state.call_count)

        def check_bad(spconf):
            """
            Check that missing or invalid remote configuration does not
            actually trigger any local events.
            """
            check_something(spconf, None, 0)

        def check_good(spdict):
            """
            Check that a well-formed remote configuration that does not have
            presence information about our own Juju node still does not
            trigger any local events, but is stored properly.
            """
            check_something(json.dumps(spdict), spdict, 0)

        def check_wonderful(spdict):
            """
            Check that a well-formed remote configuration that has our node in
            it goes the whole way.
            """
            check_something(json.dumps(spdict), spdict, 1)

        # No configuration at all supplied
        check_bad(None)

        # Invalid JSON encoding of the configuration
        check_bad('{[(')

        # Not a JSON object
        check_bad('[5]')

        # An empty dictionary
        check_good({})

        # A dictionary without us in it
        check_good({"invalid node name": True, "some other node": False})

        # A dictionary with us in it, but with a false value
        check_good({sp_node: False})

        # And finally, a dictionary with us *really* in it!
        check_wonderful({sp_node: True})
