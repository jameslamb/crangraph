#Sample code snippets for working with psycopg


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def initialize(self, conf, ctx):
    # Connect to the database
    conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")

    #Create database to tcount
    try:
	# CREATE DATABASE can't run inside a transaction
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()
	cur.execute("SELECT datname FROM pg_database WHERE datname='tcount'")
	if cur.rowcount == 0:
	    cur.execute("CREATE DATABASE tcount")
	cur.close()
	conn.close()
    except:
	self.log("Count-Bolt Exception: Could not create tcount")

    self.conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
    self.counts = Counter()
    self.cur = self.conn.cursor()
    self.cur.execute("SELECT relname FROM pg_class WHERE relname='tweetwordcount'")

    if self.cur.rowcount == 0:
	try:
	    self.cur.execute('''CREATE TABLE tweetwordcount
		   (word TEXT PRIMARY KEY     NOT NULL,
		   count INT     NOT NULL);''')
	    self.conn.commit()
	except:
	    self.log("Count-Bolt Exception: Table already created in the meanwhile")

def process(self, tup):
    word = tup.values[0]

    # Write codes to increment the word count in Postgres
    # Use psycopg to interact with Postgres
    # Database name: Tcount 
    # Table name: Tweetwordcount 
    # you need to create both the database and the table in advance.
    

    # Increment the local count
    self.counts[word] += 1
    self.emit([word, self.counts[word]])

    if self.counts[word] == 1:
	#Check if we need to insert
	#A parallel bolt could have already done the insert
	try:
	    self.cur.execute("SELECT COUNT(*) FROM tweetwordcount WHERE word =%s", (word,))
	    exists = self.cur.fetchone()[0]
	    if exists == 0:
		try:
		    self.cur.execute("INSERT INTO tweetwordcount (word,count) VALUES (%s, %s)", (word, 1))
		except:
		    self.log("Count-Bolt Exception: Row inserted by another bolt, updating instead")
		    self.cur.execute("UPDATE tweetwordcount SET count=count+1 WHERE word=%s", (word,))
	    else:
		#Update by incrementing the existing value in the table
		self.cur.execute("UPDATE tweetwordcount SET count=count+1 WHERE word=%s", (word,))
	except:
	    self.log( "Count-Bolt Exception: Skipping the word due to failure")
    else:
	#Update by incrementing the existing value in the table
	self.cur.execute("UPDATE tweetwordcount SET count=count+1 WHERE word=%s", (word,))

    self.conn.commit()

    # Log the count - just to see the topology running
    self.log('%s: %d' % (word, self.counts[word]))

if __name__ == "__main__":

    # Connect to the database
    conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
    try:
        # CREATE DATABASE can't run inside a transaction
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datname='tcount'")
        if cur.rowcount == 0:
            cur.execute("CREATE DATABASE tcount")
        cur.close()
        conn.close()
    except:
	print "Couldnt create database tcount"
