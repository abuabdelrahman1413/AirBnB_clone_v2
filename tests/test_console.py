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
import sys
import pycodestyle


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


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "tests only when in DB mode")
class test_create_console_filestorage(unittest.TestCase):
    """This class tests the create command of the console
    program
    """
    def test_create_only_cmd(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        self.assertEqual(f.getvalue(), "** class name missing **\n")

    def test_create_random_arg_cmd(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create ROBOT")
        self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

    def test_create_BaseModel_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        self.assertEqual(len(f.getvalue()), 37)
        try:
            with open('file.json', 'r', encoding='utf-8') as f:
                jsonstr = f.read()
            self.assertTrue('BaseModel' in jsonstr)
        except Exception:
            pass

    def test_create_User_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
        self.assertEqual(len(f.getvalue()), 37)

    def test_create_City_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
        self.assertEqual(len(f.getvalue()), 37)

    def test_create_State_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
        self.assertEqual(len(f.getvalue()), 37)

    def test_create_Review_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
        self.assertEqual(len(f.getvalue()), 37)

    def test_create_Place_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
        self.assertEqual(len(f.getvalue()), 37)

    def test_create_Amenity_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
        self.assertEqual(len(f.getvalue()), 37)

    def test_create_more_than_one_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity hello world")
        self.assertEqual(len(f.getvalue()), 37)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "tests only when in DB mode")
class test_all_console_db(unittest.TestCase):
    """This class tests the create command of the console
    program using db
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
        sys.stdout.flush()
        self.cur.execute('DELETE FROM place_amenity')
        self.cur.execute('DELETE FROM places')
        self.cur.execute('DELETE FROM cities')
        self.cur.execute('DELETE FROM states')
        self.cur.execute('DELETE FROM users')
        self.cur.execute('DELETE FROM amenities')
        self.cur.execute('DELETE FROM reviews')
        self.db.commit()
        self.cur.close()
        self.db.close()

    def test_all_no_args(self):
        """"""
        state = State(name="California")
        state.save()
        city = City(state_id=state.id, name="San Francisco")
        city.save()
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        place_1 = Place(user_id=user.id, city_id=city.id, name="House 1")
        place_2 = Place(user_id=user.id, city_id=city.id, name="House 2")
        place_1.save()
        place_2.save()
        amenity_1 = Amenity(name="Wifi")
        amenity_1.save()
        amenity_2 = Amenity(name="Cable")
        amenity_2.save()
        amenity_3 = Amenity(name="Oven")
        amenity_3.save()
        place_2.amenities.append(amenity_1)
        place_2.amenities.append(amenity_2)
        place_2.amenities.append(amenity_3)
        storage.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            string = f.getvalue()
        self.assertTrue("User" in string)
        self.assertTrue("Place" in string)
        self.assertTrue("State" in string)
        self.assertTrue("City" in string)
        self.assertTrue("Amenity" in string)

    def test_all_state(self):
        """"""
        state = State(name="California")
        state.save()
        city = City(state_id=state.id, name="San Francisco")
        city.save()
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        place_1 = Place(user_id=user.id, city_id=city.id, name="House 1")
        place_2 = Place(user_id=user.id, city_id=city.id, name="House 2")
        place_1.save()
        place_2.save()
        amenity_1 = Amenity(name="Wifi")
        amenity_1.save()
        amenity_2 = Amenity(name="Cable")
        amenity_2.save()
        amenity_3 = Amenity(name="Oven")
        amenity_3.save()
        place_2.amenities.append(amenity_1)
        place_2.amenities.append(amenity_2)
        place_2.amenities.append(amenity_3)
        storage.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all State")
            string = f.getvalue()
        self.assertTrue("[User]" not in string)
        self.assertTrue("[Place]" not in string)
        self.assertTrue("[State]" in string)
        self.assertTrue("[City]" not in string)
        self.assertTrue("[Amenity]" not in string)

    def test_all_user(self):
        """"""
        state = State(name="California")
        state.save()
        city = City(state_id=state.id, name="San Francisco")
        city.save()
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        place_1 = Place(user_id=user.id, city_id=city.id, name="House 1")
        place_2 = Place(user_id=user.id, city_id=city.id, name="House 2")
        place_1.save()
        place_2.save()
        amenity_1 = Amenity(name="Wifi")
        amenity_1.save()
        amenity_2 = Amenity(name="Cable")
        amenity_2.save()
        amenity_3 = Amenity(name="Oven")
        amenity_3.save()
        place_2.amenities.append(amenity_1)
        place_2.amenities.append(amenity_2)
        place_2.amenities.append(amenity_3)
        storage.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all User")
            string = f.getvalue()
        self.assertTrue("[User]" in string)
        self.assertTrue("[Place]" not in string)
        self.assertTrue("[State]" not in string)
        self.assertTrue("[City]" not in string)
        self.assertTrue("[Amenity]" not in string)

    def test_all_place(self):
        """"""
        state = State(name="California")
        state.save()
        city = City(state_id=state.id, name="San Francisco")
        city.save()
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        place_1 = Place(user_id=user.id, city_id=city.id, name="House 1")
        place_2 = Place(user_id=user.id, city_id=city.id, name="House 2")
        place_1.save()
        place_2.save()
        amenity_1 = Amenity(name="Wifi")
        amenity_1.save()
        amenity_2 = Amenity(name="Cable")
        amenity_2.save()
        amenity_3 = Amenity(name="Oven")
        amenity_3.save()
        place_2.amenities.append(amenity_1)
        place_2.amenities.append(amenity_2)
        place_2.amenities.append(amenity_3)
        storage.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all City")
            string = f.getvalue()
        self.assertTrue("[User]" not in string)
        self.assertTrue("[Place]" not in string)
        self.assertTrue("[State]" not in string)
        self.assertTrue("[City]" in string)
        self.assertTrue("[Amenity]" not in string)

    def test_all_city(self):
        """"""
        state = State(name="California")
        state.save()
        city = City(state_id=state.id, name="San Francisco")
        city.save()
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        place_1 = Place(user_id=user.id, city_id=city.id, name="House 1")
        place_2 = Place(user_id=user.id, city_id=city.id, name="House 2")
        place_1.save()
        place_2.save()
        amenity_1 = Amenity(name="Wifi")
        amenity_1.save()
        amenity_2 = Amenity(name="Cable")
        amenity_2.save()
        amenity_3 = Amenity(name="Oven")
        amenity_3.save()
        place_2.amenities.append(amenity_1)
        place_2.amenities.append(amenity_2)
        place_2.amenities.append(amenity_3)
        storage.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all City")
            string = f.getvalue()
        self.assertTrue("[User]" not in string)
        self.assertTrue("[Place]" not in string)
        self.assertTrue("[State]" not in string)
        self.assertTrue("[City]" in string)
        self.assertTrue("[Amenity]" not in string)

    def test_all_amenity(self):
        """"""
        state = State(name="California")
        state.save()
        city = City(state_id=state.id, name="San Francisco")
        city.save()
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        place_1 = Place(user_id=user.id, city_id=city.id, name="House 1")
        place_2 = Place(user_id=user.id, city_id=city.id, name="House 2")
        place_1.save()
        place_2.save()
        amenity_1 = Amenity(name="Wifi")
        amenity_1.save()
        amenity_2 = Amenity(name="Cable")
        amenity_2.save()
        amenity_3 = Amenity(name="Oven")
        amenity_3.save()
        place_2.amenities.append(amenity_1)
        place_2.amenities.append(amenity_2)
        place_2.amenities.append(amenity_3)
        storage.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Amenity")
            string = f.getvalue()
        self.assertTrue("[User]" not in string)
        self.assertTrue("[Place]" not in string)
        self.assertTrue("[State]" not in string)
        self.assertTrue("[City]" not in string)
        self.assertTrue("[Amenity]" in string)

    def test_python_code_style(self):
        """Test Python Code Style"""
        style = pycodestyle.StyleGuide(quiet=True)
        py = style.check_files(['console.py'])
        self.assertEqual(py.total_errors, 0, "Fix pep8")

    def test_doc_console(self):
        """Test DocString for Console"""
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "tests only when in DB mode")
class Console_show_test(unittest.TestCase):
    """This class tests the show command of the console
    """
    def test_show_only_cmd(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
        self.assertEqual(f.getvalue(), "** class name missing **\n")

    def test_fake_class_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show ROBOT")
        self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

    def test_valid_class_only_arg(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Review")
        self.assertEqual(f.getvalue(), "** instance id missing **\n")

    def test_review_class_arg(self):
        a = Review()
        storage.new(a)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Review {}".format(a.id))
        self.assertEqual(f.getvalue(), "{}\n".format(str(a)))

    def test_place_class_arg(self):
        a = Place()
        storage.new(a)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Place {}".format(a.id))
        self.assertEqual(f.getvalue(), "{}\n".format(str(a)))

    def test_BaseModel_class_arg(self):
        a = BaseModel()
        storage.new(a)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel {}".format(a.id))
        self.assertEqual(f.getvalue(), "{}\n".format(str(a)))

    def test_User_class_arg(self):
        a = User()
        storage.new(a)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show User {}".format(a.id))
        self.assertEqual(f.getvalue(), "{}\n".format(str(a)))

    def test_Amenity_class_arg(self):
        a = Amenity()
        storage.new(a)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Amenity {}".format(a.id))
        self.assertEqual(f.getvalue(), "{}\n".format(str(a)))

    def test_City_class_arg(self):
        a = City()
        storage.new(a)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show City {}".format(a.id))
        self.assertEqual(f.getvalue(), "{}\n".format(str(a)))

    def test_State_class_arg(self):
        a = State()
        storage.new(a)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show State {}".format(a.id))
        self.assertEqual(f.getvalue(), "{}\n".format(str(a)))

    def test_more_than_three_args(self):
        a = User()
        storage.new(a)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show City {} 4thargument".format(a.id))


if __name__ == "__main__":
    unittest.main()
