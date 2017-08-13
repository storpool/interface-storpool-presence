import json
import platform

from charmhelpers.core import hookenv
from charms import reactive

class StorPoolConfigProvides(reactive.RelationBase):
	scope = reactive.scopes.UNIT
	sp_node = platform.node()

	@reactive.hook('{provides:storpool-config}-relation-{joined,changed}')
	def changed(self):
		self.set_state('{relation_name}.available')

	@reactive.hook('{provides:storpool-config}-relation-departed')
	def departed(self):
		self.remove_state('{relation_name}.available')
	
	def configure(self, avail, rdebug=lambda s: s):
		rdebug('config-provides-configure invoked with avail {avail}'.format(avail=avail))
		data = { self.sp_node: avail, }
		rdebug('config-provides-configure sending some data out: {data}'.format(data=data))
		self.set_remote('storpool-config', json.dumps(data))
