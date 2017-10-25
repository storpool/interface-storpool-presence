import time

from charms import reactive

def rdebug(s):
    with open('/tmp/storpool-charms.log', 'a') as f:
        print('{tm} [storpool-presence-provides] {s}'.format(tm=time.ctime(), s=s), file=f)

class StorPoolPresenceProvides(reactive.RelationBase):
    scope = reactive.scopes.GLOBAL

    @reactive.hook('{provides:storpool-presence}-relation-{joined,changed}')
    def changed(self):
        rdebug('relation-joined/changed, setting the notify state to kick something off')
        self.set_state('{relation_name}.notify')
