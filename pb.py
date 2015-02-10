import psycopg2
# http://initd.org/psycopg/docs/usage.html - about psql connection

# Connect to an existing database:
conn=psycopg2.connect(
    dbname="pbook",
    user="alex",
#    host='127.0.0.1',
#    port=''
)

# Open a cursor to perform database operations:
cur = conn.cursor()
# cur.execute("DROP TABLE IF EXISTS clients;")
cur.execute("SELECT * FROM information_schema.tables WHERE table_name=%s;",
            ('clients',))
if not bool(cur.rowcount):
    cur.execute("CREATE TABLE clients (id serial PRIMARY KEY, " +
                "name varchar, phone varchar);")

cur.execute("INSERT INTO clients(name, phone) VALUES(%s, %s)", ("Alex K",
            "9206133111"))
cur.execute("INSERT INTO clients(name, phone) VALUES(%s, %s)", ("Denis Green",
            "925553333333"))
cur.execute("INSERT INTO clients(name, phone) VALUES(%s, %s)", ("Jenny",
            "0000011111"))
cur.execute("INSERT INTO clients(name, phone) VALUES(%s, %s)", ("Robbie",
            "8888883333"))

cur.execute("SELECT * FROM clients;")
# print("cur.fetchall: " + str(cur.fetchall()))
print("cur.fetchone 1: " + str(cur.fetchone()))
# print("cur.fetchone 2: " + str(cur.fetchone()))
# print("cur.fetchall: " + str(cur.fetchall()))
print ("cur.fetchmany(100): " + str(cur.fetchmany(100)))

# print ("type(conn):" + str(type(conn)))
# print ("type(cur):" + str(type(cur)))
conn.commit()
cur.close()
conn.close()

print (dir(cur))
print ("\ncur.description:"+str(cur.description))
print (cur.rowcount)
