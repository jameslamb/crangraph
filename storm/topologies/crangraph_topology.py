"""
crangraph topology
"""

# Run the code in bolts __init__.py
import bolts

# Other imports
from streamparse import Grouping, Topology
from crangraph.storm.bolts import ParseDepsBolt
from crangraph.storm.bolts import DbUpdateBolt
from crangraph.storm.spouts import PackageMetadataSpout


class crangraphTopology(Topology):
    pkg_spout = PackageMetadataSpout.spec(par=1, name="pkg-spout")
    count_bolt = ParseDepsBolt.spec(inputs={pkg_spout: Grouping.fields(['package'])},
                                    par=2,
                                    name='parse-deps-bolt')
    dbupdate_bolt = DbUpdateBolt.spec(inputs={count_bolt: Grouping.fields(['package'])},
                                    par=1,
                                    name='db-update-bolt')
