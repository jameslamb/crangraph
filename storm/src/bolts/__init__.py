import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Set up Postgres DB

# Connect to DB
conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="pass",
                        host="localhost",
                        port="5432")


# create a DB
try:
    # CREATE DATABASE can't run inside a transaction
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE crangraph")
    cur.close()
    conn.close()
except:
    pass

# Create connection to cradeps DB
pg_conn = psycopg2.connect(database="crangraph",
                           user="postgres",
                           password="pass",
                           host="localhost",
                           port="5432")
pg_cur = pg_conn.cursor()

# Create table if it doesn't exist (only works in Postgres 9.1+)
pg_cur.execute("""
                CREATE TABLE IF NOT EXISTS crandeps (
                    pkgname TEXT PRIMARY KEY NOT NULL,
                    depstr json NOT NULL
                )
               """
               )

# Be courteous and close out
pg_cur.close()
pg_conn.close()