"""
A Juju charm interface for informing another charm of the state of this
charm's units, esp. the unit running on the local node.
"""
from charms import reactive
from charmhelpers.core import unitdata

from spcharms import kvdata
from spcharms import utils as sputils


def rdebug(s):
    """
    Pass the diagnostic message string `s` to the central diagnostic logger.
    """
    sputils.rdebug(s, prefix='storpool-presence-provides')


class StorPoolPresenceProvides(reactive.RelationBase):
    """
    Send notifications for the state of our units.
    """
    scope = reactive.scopes.GLOBAL

    @reactive.hook('{provides:storpool-presence}-relation-joined')
    def joined(self):
        """
        Somebody new came in, announce our presence to them if able.
        """
        rdebug('relation-joined/changed invoked')
        self.set_state('{relation_name}.present')
        self.set_state('{relation_name}.notify')
        self.set_state('{relation_name}.notify-joined')

    @reactive.hook('{provides:storpool-presence}-relation-changed')
    def changed(self):
        """
        Somebody sent us something, process it and send stuff back?
        """
        rdebug('relation-joined/changed invoked')
        self.set_state('{relation_name}.present')
        self.set_state('{relation_name}.notify')

    @reactive.hook('{provides:storpool-presence}-relation-{departed,broken}')
    def gone_away(self):
        """
        Nobody wants to talk to us any more...
        """
        rdebug('relation-departed/broken invoked')
        self.remove_state('{relation_name}.present')
        self.remove_state('{relation_name}.notify')
        self.remove_state('{relation_name}.notify-new')
