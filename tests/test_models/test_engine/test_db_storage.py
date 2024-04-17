#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel, Base
from models.engine.db_storage import DBStorage
from models.state import State
from models.user import User
from models import storage
import os
import pycodestyle
import MySQLdb


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 'testing dbstorage only')
class test_dbstorage(unittest.TestCase):
    """ Class to test the file storage method """

    @classmethod
    def setUpClass(cls):
        """ Set up test environment """
        hst = os.getenv('HBNB_MYSQL_HOST')
        usr = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        dbname = os.getenv('HBNB_MYSQL_DB')
        db = MySQLdb.connect(host=hst, user=usr, passwd=pwd, db=dbname)
        db.autocommit(True)
        cls.cur = db.cursor()

    def tearDown(self):
        """"""
        test_dbstorage.cur.execute('DELETE FROM place_amenity')
        test_dbstorage.cur.execute('DELETE FROM places')
        test_dbstorage.cur.execute('DELETE FROM cities')
        test_dbstorage.cur.execute('DELETE FROM states')
        test_dbstorage.cur.execute('DELETE FROM users')
        test_dbstorage.cur.execute('DELETE FROM amenities')
        test_dbstorage.cur.execute('DELETE FROM reviews')

    def test_new(self):
        """ New object is correctly added to db """
        before = test_dbstorage.cur.execute('SELECT * FROM states')
        new = State(**{'name': 'CALI'})
        storage.new(new)
        storage.save()
        after = test_dbstorage.cur.execute('SELECT * FROM states')
        self.assertEqual(after - before, 1)

    def test_all(self):
        """ Objects in db are properly returned """
        new1 = State(**{'name': 'CALI'})
        new2 = User(**{'email': 'abdu.hany@gmail.com', 'password': 'mypass'})
        storage.new(new1)
        storage.new(new2)
        storage.save()
        temp = storage.all()
        self.assertIsInstance(temp, dict)
        self.assertEqual(len(temp), 2)

    def test_db_obj_instantiation(self):
        """ db doesn't change on object instantiation """
        before = test_dbstorage.cur.execute('SELECT * FROM states')
        new = State(**{'name': 'Washington'})
        after = test_dbstorage.cur.execute('SELECT * FROM states')
        self.assertEqual(before, after)

    def test_empty(self):
        """ Data is saved to db """
        before = test_dbstorage.cur.execute('SELECT * FROM states')
        new = State(**{'name': 'CALI'})
        thing = new.to_dict()
        new.save()
        new2 = State(**thing)
        after = test_dbstorage.cur.execute('SELECT * FROM states')
        self.assertEqual((after - before), 1)

    def test_save(self):
        """ DB save method """
        before = test_dbstorage.cur.execute('SELECT * FROM states')
        new = State(**{'name': 'ANY STATE NAME'})
        storage.save()
        after = test_dbstorage.cur.execute('SELECT * FROM states')
        self.assertEqual(before, after)

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = State(**{'name': 'CALI'})
        new.save()
        storage.reload()
        loaded = new
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty db """
        storage.reload()
        a = storage.all()
        self.assertEqual(a, {})

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_db_obj_save(self):
        """ BaseModel save method calls storage save """
        new = State(**{'name': 'ANOTHER STATE'})
        new.save()
        query = test_dbstorage.cur.execute('SELECT * FROM states WHERE ' +
                                           'name = "ANOTHER STATE"')
        self.assertTrue(query == 1)

    def test_type_path(self):
        """ Confirm __session is session object """
        from sqlalchemy.orm.session import Session
        self.assertEqual(str(type(storage._DBStorage__session)),
                         "<class 'sqlalchemy.orm.session.Session'>")

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = State(**{'name': 'ANOTHER STATE'})
        _id = new.to_dict()['id']
        storage.new(new)
        storage.save()
        temp = 0
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, ('State' + '.' + _id))

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)

    def test_pycode_style(self):
        """ Test for PythonCodeStyle """
        style = pycodestyle.StyleGuide(quiet=True)
        py = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(py.total_errors, 0, "fix pep8")

    def test_doc_string_db_storage(self):
        """ Test for Doc String"""
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)


if __name__ == "__main__":
    unittest.main()
