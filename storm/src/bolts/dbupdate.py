# Bolt that gets the package and dependency info from ParseDepsBolt and updates in the postgres DB
#
from __future__ import absolute_import, print_function, unicode_literals
import crangraph.utils as cgu
from streamparse.bolt import Bolt

#Sample code snippets for working with psycopg
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DbUpdateBolt(Bolt):

    outputs = [None]

    def initialize(self):

        print "Creating crangraph DB"
        # Connect to the database
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
        try:
            # CREATE DATABASE can't run inside a transaction
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute("SELECT datname FROM pg_database WHERE datname='crangraph'")
            if cur.rowcount == 0:
                cur.execute("CREATE DATABASE crangraph")
            cur.close()
            conn.close()
        except:
            print "Couldnt create database crangraph"


        print "Creating crandeps table"
        self.conn = psycopg2.connect(database="crangraph", user="postgres", password="postgres", host="localhost", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT relname FROM pg_class WHERE relname='crandeps'")

        if self.cur.rowcount == 0:
            try:
                self.cur.execute('''CREATE TABLE crandeps
                       (pkgname TEXT PRIMARY KEY NOT NULL,
                        depstr json NOT NULL);''')
                self.conn.commit()
            except:
                print "Table crandeps already created"
        pass

    def process(self, tup):
        # Get the package and dependency strings
        depstr = tup.values[0]['dependency']
        pkgname = tup.values[0]['package']

        self.cur.execute("SELECT COUNT(*) FROM crandeps WHERE pkgname =%s", (pkgname,))
        exists = self.cur.fetchone()[0]
        if exists == 0:
            try:
                self.cur.execute("INSERT INTO crandeps (pkgname, depstr) VALUES (%s, %s)", (pkgname, depstr))
            except:
                print "Package insert failed, trying update"
                self.cur.execute("UPDATE crandeps SET depstr=(%s) WHERE pkgname=(%s)", (depstr, pkgname))
        else:
            #Update by incrementing the existing value in the table
            print "Package %s exists already, updating"
            self.cur.execute("UPDATE crandeps SET depstr=(%s) WHERE pkgname=(%s)", (depstr, pkgname))

