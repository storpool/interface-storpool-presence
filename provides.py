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

    @reactive.hook('{provides:storpool-presence}-relation-{joined,changed}')
    def changed(self):
        """
        Let the other layers know that another charm wants to receive
        notifications from us.
        """
        rdebug('relation-joined/changed, setting the notify state to '
               'kick something off')
        self.set_state('{relation_name}.notify')

        conv = self.conversation()
        mach_id = conv.get_remote('cinder_machine_id')
        if mach_id is not None:
            rdebug('- got a Cinder machine id: {cid}'.format(cid=mach_id))
            parts = mach_id.split('/')
            if len(parts) == 3 and parts[1] == 'lxd':
                rdebug('- and it is a container...')
                if parts[0] == sputils.get_machine_id():
                    rdebug('- and it is ours!')
                    unitdata.kv().set(kvdata.KEY_LXD_NAME, mach_id)
                    self.set_state('{relation_name}.process-lxd-name')
                else:
                    rdebug('- but it is not ours ({mid} vs {oid})'
                           .format(mid=mach_id, oid=sputils.get_machine_id()))
            else:
                rdebug('- but it is not a container')
