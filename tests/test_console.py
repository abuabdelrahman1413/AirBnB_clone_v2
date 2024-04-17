#!/usr/bin/python3
"""This module tests the AirBnB Console program
"""
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.review import Review
from models.city import City
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
import MySQLdb
import sqlalchemy
import unittest
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "tests only when in DB mode")
class test_create_console_db(unittest.TestCase):
    """This class tests the create command of the console
    program
    """

    def setUp(self):
        """ Set up test environment """
        hst = os.getenv('HBNB_MYSQL_HOST')
        usr = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        dbname = os.getenv('HBNB_MYSQL_DB')
        self.db = MySQLdb.connect(host=hst, user=usr, passwd=pwd, db=dbname)
        self.db.autocommit(True)
        self.cur = self.db.cursor()

    def tearDown(self):
        """"""
        self.cur.execute('DELETE FROM place_amenity')
        self.cur.execute('DELETE FROM places')
        self.cur.execute('DELETE FROM cities')
        self.cur.execute('DELETE FROM states')
        self.cur.execute('DELETE FROM users')
        self.cur.execute('DELETE FROM amenities')
        self.cur.execute('DELETE FROM reviews')
        self.db.commit()

    def test_create_state_name(self):
        before = self.cur.execute('SELECT * FROM states')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Pennsylvania"')
        after = self.cur.execute('SELECT * FROM states')
        self.assertEqual(after - before, 1)

    def test_create_2_objects(self):
        before = self.cur.execute('SELECT * FROM states')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Pennsylvania"')
            key = f.getvalue().replace('\n', '')
            HBNBCommand().onecmd('create City state_id="{}" name="Philly"'.
                                 format(key))
        afters = self.cur.execute('SELECT * FROM states')
        afterc = self.cur.execute('SELECT * FROM cities')
        self.assertEqual(afters+afterc, 2)

    def test_create_3_objects(self):
        before = self.cur.execute('SELECT * FROM states')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Pennsylvania"')
            state_id = f.getvalue().replace('\n', '')
            HBNBCommand().onecmd('create City name="Philly" state_id="{}"'.
                                 format(state_id))
            HBNBCommand().onecmd('create User email="Abdu.hany@gmail.com" ' +
                                 'password="STRONGPASS"')
        afters = self.cur.execute('SELECT * FROM states')
        afterc = self.cur.execute('SELECT * FROM cities')
        afteru = self.cur.execute('SELECT * FROM users')
        self.assertEqual(afters+afterc+afteru, 3)


if __name__ == "__main__":
    unittest.main()
