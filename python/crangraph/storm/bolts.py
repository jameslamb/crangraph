# Bolt that parses a DESCRIPTION file and emits 

from __future__ import absolute_import, print_function, unicode_literals

import crangraph.utils as cgu
import json
import psycopg2
from streamparse.bolt import Bolt

# Bolt 1: take in descriptions and write out a set of relationship tuples
class ParseDepsBolt(Bolt):

    outputs = ['package', 'dependencies']

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
        self.log('Parsed deps: ' + pkg_name)
        out_tup = (pkg_name, deps)
        self.emit(out_tup)

# Bolt 2: Take in parsed tuples and update DB
class DbUpdateBolt(Bolt):

    outputs = ['none']

    def initialize(self, conf, ctx):
        self.conn = psycopg2.connect(database="crangraph",
                                     user="postgres",
                                     password="pass",
                                     host="localhost",
                                     port="5432")
        self.cur = self.conn.cursor()

    def process(self, tup):
        # Get the package and dependency strings
        depstr = json.dumps({'dependencies': tup.values[1]})
        pkgname = tup.values[0]

        # Add dependencies into the database
        self.cur.execute("SELECT COUNT(*) FROM crandeps WHERE pkgname =%s", (pkgname,))
        exists = self.cur.fetchone()[0]
        if exists == 0:
            try:
                self.cur.execute("INSERT INTO crandeps (pkgname, depstr) VALUES (%s, %s)", (pkgname, depstr))
            except:
                self.log("Package insert failed, trying update")
                self.cur.execute("UPDATE crandeps SET depstr=(%s) WHERE pkgname=(%s)", (depstr, pkgname))
        else:
            # Update by incrementing the existing value in the table
            self.log("Package %s exists already, updating")
            self.cur.execute("UPDATE crandeps SET depstr=(%s) WHERE pkgname=(%s)", (depstr, pkgname))

        # Be sure we commit DB operations
        self.conn.commit()
