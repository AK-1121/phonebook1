import unittest
from pb import DB
from settings import *


class TestPhoneBook(unittest.TestCase):

    def setUp(self):
        self.p_db = DB(DB_NAME, USER, HOST, PSWD)

    # Tested methods:
    # check_table(), number_of_records(), add_record()
    def test_check_table(self):
        self.p_db.check_table()
        number1 = self.p_db.number_of_records()
        self.assertTrue(number1 >= 0)
        self.p_db.add_record("Monika", "344 345 3456")
        self.p_db.add_record("Lisa Simpson", "456-345-2345")
        self.assertTrue(self.p_db.number_of_records()-number1 == 2)

    # Tested methods:
    # del_all(), add_record(), find_all(), find_by_field('name', ...),
    # find_by_field('phone', ...)
    def test_add_record(self):
        self.p_db.del_all()
        self.p_db.add_record("Alex", "3334444")
        self.assertIn("Alex", str(self.p_db.find_all()))
        self.assertIn("3334444", str(self.p_db.find_all()))
        self.p_db.add_record("Tom Rock Jr.", "8 (742) 345-12-11")
        self.assertIn("87423451211",
                      str(self.p_db.find_by_field('name', "Tom Rock Jr.")))
        self.assertEqual("Phone number is not correct. Can`t add this record.",
                         self.p_db.add_record("Jim", "8234test8324"))
        self.assertEqual([], self.p_db.find_by_field("phone", "8234test8324"))

    # Tested methods:
    # del_all(), load_from_file()
    def test_load_from_file(self):
        self.p_db.del_all()
        # index1.txt - doesn`t existl; input.txt - exists:
        self.assertEqual("I can`t find this file.",
                         self.p_db.load_from_file("index1.txt"))
        self.assertEqual("Loading successfully finished.",
                         self.p_db.load_from_file("input.txt"))

    def tearDown(self):
        self.p_db.close_db()


if __name__ == '__main__':
    unittest.main()
