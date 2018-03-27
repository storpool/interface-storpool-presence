The storpool-presence interface format
======================================

JSON message format
-------------------

    {
      "presence": {
        "<service-name>": {
          "<juju-node-id>": "<storpool-our-id>",
          "<juju-node-id>": "<storpool-our-id>"
        },
        "<service-name>": {
          "<juju-node-id>": "<storpool-our-id>",
          "<juju-node-id>": "<storpool-our-id>"
        },
      "storpool_version": "<version of the StorPool package in the PPA>",
      "storpool_openstack_version": "<version of the StorPool OpenStack integration package in the PPA>",
      "storpool_conf": "<multiline contents of the /etc/storpool.conf file>"
    }

Fields description
------------------

- `service-name`: the type of the charm that is announcing its presence,
   e.g. "block" or "cinder".

- `juju-node-id`: the machine ID or the LXC ID that the service unit is
   running on, e.g. "0" or "1/lxd/2".

- `storpool-our-id`: the StorPool `SP_OURID` client ID used by this unit;
   the `storpool-block` charm determines its value from the `storpool_conf`
   setting, and the `cinder-storpool` charm uses the same value as
   the `storpool-block` unit running on bare metal on the node that hosts
   the `cinder-storpool` unit's container.  Thus, if `storpool-block` has
   announced e.g. `SP_OURID` "3" on node "0", the `cinder-storpool` unit
   running in the "0/lxd/2" container will use "3" as its own ID.

- `storpool_version`: the version number (or rather, string) of
   the `storpool-common`, `storpool-config`, et al packages that will be
   installed from the StorPool PPA.

- `storpool_openstack_version`: the version number (or rather, string) of
   the `storpool-openstack-integration` package that will be installed from
   the StorPool PPA.

- `storpool_conf`: the contents of the `/etc/storpool.conf` file that
   the units will install for the StorPool services and Python bindings.
