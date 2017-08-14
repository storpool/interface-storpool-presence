import json
import platform
import re
import time
import subprocess

from charms import reactive

def rdebug(s):
	with open('/tmp/storpool-charms.log', 'a') as f:
		print('{tm} [storpool-config-requires] {s}'.format(tm=time.ctime(), s=s), file=f)

class StorPoolRepoRequires(reactive.RelationBase):
	scope = reactive.scopes.UNIT
	sp_node = platform.node()

	@reactive.hook('{requires:storpool-config}-relation-{joined,changed}')
	def changed(self):
		rdebug('relation-joined/changed invoked')
		conv = self.conversation()
		spconf = conv.get_remote('storpool-config')
		if spconf is None:
			rdebug('no config yet')
			conv.set_local('storpool-config', None)
			self.remove_state('{relation_name}.available')
		else:
			rdebug('whee, we got something from the {key} conversation, trying to deserialize it'.format(key=conv.key))
			try:
				conf = json.loads(spconf)
				rdebug('got something: type {t}, dict keys: {k}'.format(t=type(conf).__name__, k=sorted(conf.keys()) if isinstance(conf, dict) else []))
				if not isinstance(conf, dict):
					rdebug('well, it is not a dictionary, is it?')
					conv.set_local('storpool-config', None)
					return
				conv.set_local('storpool-config', conf)
				if self.sp_node in conf:
					rdebug('we have some configuration for our node!')
					self.set_state('{relation_name}.available')
			except Exception as e:
				rdebug('oof, could not parse the config passed down the hook: {e}'.format(e=e))
				conv.set_local('storpool-config', None)

	@reactive.hook('{requires:storpool-config}-relation-departed')
	def departed(self):
		conv = self.conversation()
		c = conv.get_local('storpool-config')
		if c is not None and isinstance(c, dict):
			ks = sorted(c.keys())
			rdebug('oof, departed invoked for {ks}'.format(ks=ks))
			if self.sp_node in ks:
				rdebug('...and it was on our node, no less')
				self.remove_state('{relation_name}.available')
		conv.set_local('storpool-config', None)
	
	def get_storpool_config(self):
		cfg = None
		for conv in self.conversations():
			ncfg = conv.get_local('storpool-config')
			if ncfg is not None:
				nkeys = list(sorted(ncfg.keys()))
				rdebug('get_storpool_config(): {key}: {ks}'.format(key=conv.key, ks=nkeys))
				if cfg is not None:
					for key in nkeys:
						cfg[key] = ncfg[key]
				else:
					cfg = ncfg
		if cfg is not None:
			rdebug('get_storpool_config() returning keys: {ks}'.format(ks=sorted(cfg.keys())))
		return cfg
