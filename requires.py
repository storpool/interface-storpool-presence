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
    sp_node = platform.node()

    @reactive.hook('{requires:storpool-presence}-relation-{joined,changed}')
    def changed(self):
        """
        Handle a notification and set the "*.configure" state if the unit
        running on the local node has been set up.
        """
        rdebug('relation-joined/changed invoked')
        conv = self.conversation()
        spconf = conv.get_remote('storpool_presence')
        conv.set_local('storpool_presence', None)
        reset = False
        if spconf is None:
            rdebug('no presence data yet')
        else:
            rdebug('whee, we got something from the {key} conversation, '
                   'trying to deserialize it'.format(key=conv.key))
            try:
                conf = json.loads(spconf)
                rdebug('got something: type {t}, dict keys: {k}'
                       .format(t=type(conf).__name__,
                               k=sorted(conf.keys()) if isinstance(conf, dict)
                               else []))
                if not isinstance(conf, dict):
                    rdebug('well, it is not a dictionary, is it?')
                    return
                presence = conf.get('presence', None)
                if not isinstance(presence, dict):
                    rdebug('no presence data, just {keys}'
                        .format(keys=','.join(sorted(conf.keys()))))
                    return
                rdebug('configured nodes: {nodes}'
                       .format(nodes=','.join(sorted(presence.keys()))))
                conv.set_local('storpool_presence', conf)
                reset = True

                for key in STORPOOL_CONF_KEYS:
                    data = conf.get(key, None)
                    if data is None or data == '':
                        rdebug('- {key} not supplied yet'.format(key=key))
                        return
                if presence.get(self.sp_node, False):
                    rdebug('our node seems to be configured!')
                    self.set_state('{relation_name}.configure')
            except Exception as e:
                rdebug('oof, could not parse the presence data passed down '
                       'the hook: {e}'.format(e=e))
                if reset:
                    conv.set_local('storpool_presence', None)
