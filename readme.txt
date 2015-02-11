My little phonebook.

Using:
    - Python3 + postgresql;
    - psycopg2 - for making communications with DB 
      ( https://pypi.python.org/pypi/psycopg2 )

Database name:  pbook
table name:     clients
user name:      alex

Access configuration: peer for local connections:
/etc/postgresql/9.3/main/pg_hba.conf

...
# Database administrative login by Unix domain socket
local   all             postgres                                peer
# TYPE  DATABASE        USER            ADDRESS                 METHOD
# "local" is for Unix domain socket connections only
local   all             all                                     peer
...

