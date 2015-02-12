import psycopg2
import re
from settings import *

# http://initd.org/psycopg/docs/usage.html - about psql connection


class DB:
    def __init__(self, dbname, user, host='', pswd=''):
        self.conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=pswd)
        self.cur = self.conn.cursor()

    # Check the existance of the clients table in the phonebook  (+ create it).
    def check_table(self):
        # Check existance of table clients:
        self.cur.execute("SELECT * FROM information_schema.tables WHERE" +
                         " table_name='clients';")

        # Create a table if it does not exist:
        if not bool(self.cur.rowcount):
            self.cur.execute("CREATE TABLE clients (id serial PRIMARY KEY, " +
                             "name varchar, phone varchar);")

    # Show number of records in the phonebook:
    def number_of_records(self):
        self.cur.execute("SELECT * FROM clients")
        return len(self.cur.fetchall())

    # Find record in the PB by one of the fields:
    def find_by_field(self, field, name):
        self.cur.execute("SELECT * FROM clients WHERE "+field+"=%s;", (name, ))
        return(self.cur.fetchall())

    # Show all records in the phonebook:
    def find_all(self):
        self.cur.execute("SELECT * FROM clients;")
        return(self.cur.fetchall())

    # Add record to the phonebook:
    def add_record(self, name, phone):
        phone = clean_phone(phone)
        if not phone.isdigit():
            return "Phone number is not correct. Can`t add this record."
        self.cur.execute("INSERT INTO clients(name, phone) VALUES(%s, %s)",
                         (name, phone))
        self.conn.commit()
        return "Record was successfully added."

    # Load file with phone records to our phonebook:
    def load_from_file(self, f_name):
        try:
            self.file = open(f_name, "r")
        except:
            return "I can`t find this file."
        text = self.file.readlines()
        correct_records = []

        for i in text:
            i = re.sub(' +', ' ', i)  # Remove double spaces.
            if re.match("[ .A-za-z\-`]+\s*[0-9() \-]{5,15}", i):
                correct_records.append(i)

        for r in correct_records:
            name = re.search("([ .A-Za-z\-`]+)", r).groups()[0].strip(" ")
            phone = clean_phone(re.search("([0-9() \-]{5,15})", r)
                                .groups()[0].strip(" "))
            self.cur.execute("INSERT INTO clients(name, phone) VALUES(%s, %s)",
                             (name, phone))
        self.conn.commit()
        self.file.close()
        return "Loading successfully finished."

    # Delete all records from the phonebook:
    def del_all(self):
        self.cur.execute("DELETE FROM clients;")
        self.conn.commit()
        self.cur.execute("SELECT * FROM clients;")
        return(self.cur.fetchall())

    # Close connection with phonebook database:
    def close_db(self):
        self.cur.close()
        self.conn.close()


# Convert list to formatted string while printing:
def conv_to_str(list1):
    return str(list1).strip('[]').replace('), (', '\n').strip('()')


# Clean phone number from marking symbols:
def clean_phone(phone):
    return re.sub("[() \-\s]", "", phone)

if __name__ == '__main__':
    p_db = DB(DB_NAME, USER, HOST, PSWD)
    p_db.check_table()
    flag = True
    while flag:
        print("="*30+"\nWelcome to my phonebook! \n\nWhat do you want to do?")
        print("s - show list; \nn - find by name;\np - find by phone;")
        print("a - add a new record;\nl - load from file;")
        print("e - erase all book.\n")
        key = input(" Choose --> ")

        if key == "s":
            print("This is the hole phonebook:")
            print(conv_to_str(p_db.find_all()))

        elif key == 'n':
            name = input("Give me a name:")
            list_of_fetch_records = p_db.find_by_field('name', name)
            if len(list_of_fetch_records) == 0:
                print("\nThere are no such records.\n")
            else:
                print(conv_to_str(list_of_fetch_records))

        elif key == 'p':
            phone = input("Give me a phone number:")
            list_of_fetch_records = p_db.find_by_field('phone', phone)
            if len(list_of_fetch_records) == 0:
                print("\nThere are no such records.\n")
            else:
                print(conv_to_str(list_of_fetch_records))

        elif key == 'a':
            name = input("Give me a name:")
            phone = input("Give me a phone number:")
            print(p_db.add_record(name, phone))

        elif key == 'l':
            file_name = input("Give a file name (input.txt - default):")
            if not file_name:
                file_name = "input.txt"
            print(p_db.load_from_file(file_name))

        elif key == 'e':
            p_db.del_all()
            print("\nThe phonebook was erased.\n")

        key = input("\n"+"="*30+"\nPress 'q' to quit." +
                    "\nPress any other key to continue:")
        if key == 'q':
            p_db.close_db()
            flag = False
