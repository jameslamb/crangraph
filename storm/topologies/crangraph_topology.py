"""
crangraph topology
"""

from streamparse import Grouping, Topology
from crangraph.storm.bolts import ParseDepsBolt
from crangraph.storm.spouts import PackageMetadataSpout


class crangraphTopology(Topology):
    pkg_spout = PackageMetadataSpout.spec(par=1, name="pkg-spout")
    count_bolt = ParseDepsBolt.spec(inputs={pkg_spout: Grouping.fields(['package'])},
                                    par=2,
                                    name='parse-deps-bolt')