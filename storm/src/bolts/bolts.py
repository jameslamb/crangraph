# Bolt that parses a DESCRIPTION file and emits 

from __future__ import absolute_import, print_function, unicode_literals

import crangraph.utils as cgu
from streamparse.bolt import Bolt

# Bolt 1: take in descriptions and write out a set of relationship tuples
class ParseDepsBolt(Bolt):

    outputs = ['package', 'dependency']

    def initialize(self, conf, ctx):
        pass

    def process(self, tup):

        # Grab description
        pkg_name = tup.values[0]['package']
        pkg_description = tup.values[0]['description']

        # Parse dependencies
        deps = cgu.scrape_deps_from_description(pkg_description)

        # emit package-dependency tuples
        self.emit_many([{'package': pkg_name, 'dependency': dep} for dep in deps])
        self.log([{'package': pkg_name, 'dependency': dep} for dep in deps])
