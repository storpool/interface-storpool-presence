from charms import reactive

from spcharms import utils as sputils


def rdebug(s):
    sputils.rdebug(s, prefix='storpool-presence-provides')


class StorPoolPresenceProvides(reactive.RelationBase):
    scope = reactive.scopes.GLOBAL

    @reactive.hook('{provides:storpool-presence}-relation-{joined,changed}')
    def changed(self):
        rdebug('relation-joined/changed, setting the notify state to '
               'kick something off')
        self.set_state('{relation_name}.notify')
