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
        pkg_name = tup.values[0].encode('utf-8')
        pkg_description = tup.values[1].encode('utf-8')
        self.log(pkg_name)

        # Parse dependencies
        deps = cgu.scrape_deps_from_description(pkg_description)

        # emit package-dependency tuples
        out_tups = [(pkg_name, dep) for dep in deps]
        for tup in out_tups:
            self.emit(tup)