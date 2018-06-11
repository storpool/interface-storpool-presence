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

    def set_notify_states(self, joined):
        """
        Set the "notify" state and optionally the "notify-joined" one.
        """
        self.set_state('{relation_name}.notify')
        if joined:
            self.set_state('{relation_name}.notify-joined')

    @reactive.hook('{provides:storpool-presence}-relation-joined')
    def joined(self):
        """
        Somebody new came in, announce our presence to them if able.
        """
        rdebug('relation-joined invoked')
        self.set_notify_states(True)

    @reactive.hook('{provides:storpool-presence}-relation-changed')
    def changed(self):
        """
        Somebody sent us something, process it, but don't send anything.
        """
        rdebug('relation-changed invoked')
        self.set_notify_states(False)

    @reactive.hook('{provides:storpool-presence}-relation-departed')
    def gone_away(self):
        """
        Somebody went away, figure out if we need to deconfigure anything.
        """
        rdebug('relation-departed invoked')
        self.set_notify_states(False)

    @reactive.hook('{provides:storpool-presence}-relation-broken')
    def softly_and_suddenly_vanished_away(self):
        """
        Everybody went away, we probably need to deconfigure something.
        """
        rdebug('relation-broken invoked')
        self.set_notify_states(False)
