import json
import platform
import time

from charmhelpers.core import hookenv
from charms import reactive

def rdebug(s):
	with open('/tmp/storpool-charms.log', 'a') as f:
		print('{tm} [storpool-config-provides] {s}'.format(tm=time.ctime(), s=s), file=f)

class StorPoolConfigProvides(reactive.RelationBase):
	scope = reactive.scopes.UNIT
	sp_node = platform.node()

	@reactive.hook('{provides:storpool-config}-relation-{joined,changed}')
	def changed(self):
		self.set_state('{relation_name}.available')

	@reactive.hook('{provides:storpool-config}-relation-departed')
	def departed(self):
		self.remove_state('{relation_name}.available')
	
	def configure(self, nodedata, extra_hostname=None):
		rdebug('config-provides-configure invoked with {ks} keys'.format(ks=len(nodedata.keys())))
		data = { self.sp_node: nodedata, }
		if extra_hostname is not None:
			data[extra_hostname] = nodedata
		rdebug('config-provides-configure sending some data out, keys: {ks}'.format(ks=sorted(data.keys())))
		self.set_remote('storpool-config', json.dumps(data))
