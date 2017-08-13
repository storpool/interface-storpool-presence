import json
import re
import time
import subprocess

from charms import reactive

def rdebug(s):
	with open('/tmp/storpool-charms.log', 'a') as f:
		print('{tm} [storpool-config-requires] {s}'.format(tm=time.ctime(), s=s), file=f)

class StorPoolRepoRequires(reactive.RelationBase):
	scope = reactive.scopes.UNIT

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
				rdebug('got something: type {t}, value {conf}'.format(t=type(conf).__name__, conf=conf))
				conv.set_local('storpool-config', conf)
				self.set_state('{relation_name}.available')
			except Exception as e:
				rdebug('oof, could not parse the config passed down the hook')
				conv.set_local('storpool-config', None)

	@reactive.hook('{requires:storpool-config}-relation-departed')
	def departed(self):
		rdebug('oof, departed invoked')
		conv = self.conversation()
		rdebug('conv is {conv}'.format(conv=conv))
		conv.set_local('storpool-config', None)
		self.remove_state('{relation_name}.available')
	
	def get_storpool_config(self):
		cfg = None
		for conv in self.conversations():
			ncfg = conv.get_local('storpool-config')
			if ncfg is not None:
				nkeys = list(sorted(ncfg.keys()))
				rdebug('got some config from the {key} conversation; keys: {nkeys}'.format(key=conv.key, nkeys=nkeys))
				if cfg is not None:
					for key in nkeys:
						if key in cfg:
							rdebug('oof, double config for key {key}, will override'.format(key=key))
						cfg[key] = ncfg[key]
				else:
					rdebug('stashing what we just got')
					cfg = ncfg
		rdebug('and in the end, cfg is {xnot}None'.format(xnot='' if cfg is None else 'not '))
		if cfg is not None:
			rdebug('...and returning keys: {ks}'.format(ks=sorted(cfg.keys())))
		return cfg
