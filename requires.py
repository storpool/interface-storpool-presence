import json
import platform
import re
import time
import subprocess

from charms import reactive

def rdebug(s):
	with open('/tmp/storpool-charms.log', 'a') as f:
		print('{tm} [storpool-presence-requires] {s}'.format(tm=time.ctime(), s=s), file=f)

class StorPoolPresenceRequires(reactive.RelationBase):
	scope = reactive.scopes.GLOBAL
	sp_node = platform.node()

	@reactive.hook('{requires:storpool-presence}-relation-{joined,changed}')
	def changed(self):
		rdebug('relation-joined/changed invoked')
		conv = self.conversation()
		spconf = conv.get_remote('storpool_presence')
		if spconf is None:
			rdebug('no presence data yet')
			conv.set_local('storpool_presence', None)
		else:
			rdebug('whee, we got something from the {key} conversation, trying to deserialize it'.format(key=conv.key))
			try:
				conf = json.loads(spconf)
				rdebug('got something: type {t}, dict keys: {k}'.format(t=type(conf).__name__, k=sorted(conf.keys()) if isinstance(conf, dict) else []))
				if not isinstance(conf, dict):
					rdebug('well, it is not a dictionary, is it?')
					conv.set_local('storpool_presence', None)
					return
				conv.set_local('storpool_presence', conf)
				if conf.get(self.sp_node, False):
					rdebug('our node seems to be configured!')
					self.set_state('{relation_name}.configure')
			except Exception as e:
				rdebug('oof, could not parse the presence data passed down the hook: {e}'.format(e=e))
				conv.set_local('storpool_presence', None)
