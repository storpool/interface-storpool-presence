"""
A Juju charm interface for informing another charm of the state of this
charm's units, esp. the unit running on the local node.
"""
from charms import reactive
from charmhelpers.core import unitdata

from spcharms import kvdata
from spcharms import service_hook
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

    @reactive.hook('{provides:storpool-presence}-relation-{joined,changed}')
    def changed(self):
        """
        Somebody came in or gave us new data.
        """
        rdebug('storpool-presence/changed invoked')
        service_hook.handle_remote_presence(self, rdebug=rdebug)

    @reactive.hook('{provides:storpool-presence}-relation-{departed,broken}')
    def broken(self):
        """
        Let it go...
        """
        rdebug('storpool-presence/departed invoked')
        self.remove_state('{relation_name}.notify')
