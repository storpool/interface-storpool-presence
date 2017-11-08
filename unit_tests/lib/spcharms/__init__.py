#!/usr/bin/python

import mock

utils = mock.Mock()
utils.MACHINE_ID = '42'
utils.PARENT_NODE = '42'
utils.get_machine_id.return_value = utils.MACHINE_ID
utils.get_parent_node.return_value = utils.PARENT_NODE

kvdata = mock.Mock()
kvdata.KEY_LXD_NAME = 'storpool-openstack-integration.lxd-name'
