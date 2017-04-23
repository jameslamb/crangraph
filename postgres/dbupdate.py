#Sample code snippets for working with psycopg
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


if __name__ == "__main__":

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
    conn = psycopg2.connect(database="crangraph", user="postgres", password="postgres", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT relname FROM pg_class WHERE relname='crandeps'")

    if cur.rowcount == 0:
	try:
	    cur.execute('''CREATE TABLE crandeps
		   (pkgname TEXT PRIMARY KEY NOT NULL,
		    depstr json NOT NULL);''')
	    conn.commit()
	except:
	    print "Table crandeps already created"

    print "Inserting a sample record"
    deps = {"lattice": ["grid", "grDevices", "graphics", "stats", "utils"]}
    depstr = json.dumps(deps)
    pkgname = 'lattice'

    cur.execute("SELECT COUNT(*) FROM crandeps WHERE pkgname =%s", (pkgname,))
    exists = cur.fetchone()[0]
    if exists == 0:
        try:
            cur.execute("INSERT INTO crandeps (pkgname, depstr) VALUES (%s, %s)", (pkgname, depstr))
        except:
            print "Package insert failed, trying update"
            cur.execute("UPDATE crandeps SET depstr=(%s) WHERE pkgname=(%s)", (depstr, pkgname))
    else:
        #Update by incrementing the existing value in the table
        print "Package %s exists already, updating"
        cur.execute("UPDATE crandeps SET depstr=(%s) WHERE pkgname=(%s)", (depstr, pkgname))

    print "Updating a sample record"
    deps = {"lattice": ["grid", "grDevices", "graphics", "stats", "utils"]}
    depstr = json.dumps(deps)
    print depstr
    pkgname = 'lattice'
    cur.execute("UPDATE crandeps SET depstr=(%s) WHERE pkgname=(%s)", (depstr, pkgname))

    print "Querying a sample record"
    cur.execute("SELECT depstr FROM crandeps WHERE pkgname =%s", (pkgname,))
    print cur.fetchone()[0]

    print "Deleting a sample record"
    cur.execute("DELETE FROM crandeps WHERE pkgname =%s", (pkgname,))

