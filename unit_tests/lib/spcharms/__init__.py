#!/usr/bin/python

import mock

utils = mock.Mock()
utils.rdebug = mock.Mock()

service_hook = mock.Mock()
service_hook.handle_remote_presence = mock.Mock()
