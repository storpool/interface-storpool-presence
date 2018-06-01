"""
A Juju charm interface for keeping track of the state of another charm's
units, esp. the state of the unit running on the local node.
"""
import json
import platform

from charms import reactive

from spcharms import utils as sputils

STORPOOL_CONF_KEYS = (
    'storpool_conf',
    'storpool_version',
    'storpool_openstack_version',
)

def rdebug(s):
    """
    Pass the diagnostic message string `s` to the central diagnostic logger.
    """
    sputils.rdebug(s, prefix='storpool-presence-requires')


class StorPoolPresenceRequires(reactive.RelationBase):
    """
    Receive notifications for another charm's units state.
    """
    scope = reactive.scopes.GLOBAL

    @reactive.hook('{requires:storpool-presence}-relation-joined')
    def joined(self):
        """
        Somebody new came in, announce our presence to them if able.
        """
        rdebug('relation-joined/changed invoked')
        self.set_state('{relation_name}.present')
        self.set_state('{relation_name}.notify')
        self.set_state('{relation_name}.notify-new')

    @reactive.hook('{requires:storpool-presence}-relation-changed')
    def changed(self):
        """
        Somebody sent us something, process it and send stuff back?
        """
        rdebug('relation-joined/changed invoked')
        self.set_state('{relation_name}.present')
        self.set_state('{relation_name}.notify')

    @reactive.hook('{requires:storpool-presence}-relation-{departed,broken}')
    def gone_away(self):
        """
        Nobody wants to talk to us any more...
        """
        rdebug('relation-departed/broken invoked')
        self.remove_state('{relation_name}.present')
        self.remove_state('{relation_name}.notify')
        self.remove_state('{relation_name}.notify-new')
