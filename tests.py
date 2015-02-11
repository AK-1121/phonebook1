import unittest
#import pb
from pb import DB

class TestPhoneBook(unittest.TestCase):

    def setUp(self):
        self.p_db = DB('pbook', 'alex')
        #self.conn = psycopg2.connect(dbname='pbook', user='alex')
        #self.cur = self.conn.cursor()

    def test_check_table(self):
        self.p_db.check_table()
        self.assertTrue(self.p_db.number_of_records()>=0)




    def tearDown(self):
        #self.cur.close()
        #self.conn.close()
        self.p_db.close_db()


if __name__ == '__main__':
    unittest.main()
