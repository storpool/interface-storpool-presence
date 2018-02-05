"""
A Juju charm interface for keeping track of the state of another charm's
units, esp. the state of the unit running on the local node.
"""
import json
import platform

from charms import reactive
from charmhelpers.core import unitdata

from spcharms import kvdata
from spcharms import service_hook
from spcharms import utils as sputils

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

    @reactive.hook('{requires:storpool-presence}-relation-{joined,changed}')
    def changed(self):
        """
        Handle a notification and set the "*.configure" state if the unit
        running on the local node has been set up.
        """
        rdebug('storpool-presence relation-joined/changed invoked')
        service_hook.handle_remote_presence(self, rdebug=rdebug)

    @reactive.hook('{requires:storpool-presence}-relation-{departed,broken}')
    def changed(self):
        """
        Remove the "we are here" state.
        """
        rdebug('storpool-presence relation-departed/broken invoked')
        self.remove_state('{relation_name}.notify')
