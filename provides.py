"""
A Juju charm interface for informing another charm of the state of this
charm's units, esp. the unit running on the local node.
"""
from charms import reactive

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
        Let the other layers know that another charm wants to receive
        notifications from us.
        """
        rdebug('relation-joined/changed, setting the notify state to '
               'kick something off')
        self.set_state('{relation_name}.notify')
