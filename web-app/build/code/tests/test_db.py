
# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
from datetime import datetime
# import json

from src.db import *
from src.app import create_app
from src.op_exceptions import AttributeRequired


config = {
    'SQLALCHEMY_DATABASE_URI': ''
}

class TestName(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_name_type(self):
        print "test_name_type"
        new_name = Name("John")
        # correct name
        self.assertEqual(new_name.value, "John")
        # incorrect name
        self.assertRaises(TypeError, Name, "123dasd")

class TestEmail(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_email_type(self):
        print "test_email_type"
        new_email = Email("smith@gmail.com")
        # correct name
        self.assertEqual(new_email.value, "smith@gmail.com")
        # incorrect name
        self.assertRaises(TypeError, Email, "@@@@smithgmail.com")

class TestUser(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation_without_role(self):
        print "test_user_creation_without_role"
        with self.assertRaises(AttributeRequired):
            user = User(name=Name("Robin Smith"), 
                            email=Email("smith@gmail.com"))

    def test_user_creation_with_role(self):
        print "test_user_creation_with_role"
        role = Role(name=Name("admin"))
        role.save()
        user = User(name=Name("Robin Smith"), 
                    email=Email("smith@gmail.com"),
                    role=Role.get_by_id(1))
        user.save()
        self.assertEqual(user.role.name, "admin")   

    def test_set_toles_to_user(self):
        print "test_set_toles_to_user"
        role = Role(name=Name("admin"))
        role.save()
        user = User(name=Name("Robin Smith"), 
                    email=Email("smith@gmail.com"),
                    role=Role.get_by_id(1))
        user.save()
        role = Role(name=Name("user"))
        user.set_role(role)
        user.save()
        users = User.get_all()
        self.assertEqual(users[0].role.name, "user")

    def test_user_get_all(self):
        print "test_user_get_all"
        role = Role(name=Name("admin"))
        role.save()
        user = User(name=Name("Termite"), 
                    email=Email("tremite@gmail.com"),
                    role=role)
        user.save()
        users = User.get_all()
        self.assertEqual("admin", users[0].role.name)

    def test_get_user_by_id(self):
        print "test_get_user_by_id"
        user = User(name=Name("Robin Smith"), 
                    email=Email("smith@gmail.com"),
                    role=Role(name=Name("admin")))
        user.save()
        self.assertEqual(user.get_by_id(1).role.name, "admin")
        self.assertEqual(user.get_by_id(1).name, "Robin Smith")

    def test_update_user(self):
        print "test_update_role"
        user = User(name=Name("Robin Smith"), 
                    email=Email("smith@gmail.com"),
                    role=Role(name=Name("admin")))
        user.save()
        u1 = User.get_by_id(1)
        print u1.to_client()
        u1.update(name=Name("Duddley Rod"), 
                  email=Email("duddley@gmail.com"),
                  role=Role(name=Name("user")))
        print u1.to_client()
        self.assertEqual(u1.get_by_id(1).name, "Duddley Rod")
        self.assertEqual(u1.get_by_id(1).role.name, "user")

class TestRole(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_role_creation(self):
        print "test_role_creation"
        role = Role(name=Name("admin"))
        role.save()
        self.assertEqual(role.name, "admin")

    def test_role_set_name(self):
        print "test_role_set_name"
        role = Role(name=Name("admin"))
        role.save()
        role.set_name(Name("user"))
        role.save()
        role = Role.get_by_id(1)
        self.assertEqual(role.name, "user")

    def test_set_users_to_role(self):
        print "test_set_users_to_role"

    def test_get_role_by_id(self):
        print "test_get_role_by_id"
        role = Role(name=Name("admin"))
        role.save()
        self.assertEqual(role.get_by_id(1).name, "admin")

    def test_update_role(self):
        print "test_update_role"
        role = Role(name=Name("admin"))
        role.save()
        rl = Role.get_by_id(1)
        rl.update(name=Name("user"))
        self.assertEqual(rl.get_by_id(1).name, "user")

    def test_role_get_all(self):
        print "test_role_get_all"
        role = Role(name=Name("admin"))
        role.save()
        roles = Role.get_all()
        self.assertEqual("admin", roles[0].name)

class TestSession(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        #setUp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        #tearDown()

    def test_session_creation(self):
        self.setUp()
        role = Role(name=Name("user"))
        role.save()
        u = User(name=Name("xyz"), 
                email=Email("xyz@gmail.com"), 
                role=Role.get_by_id(1))
        s = Session(user = u)
        self.assertEquals(s.user.email, "xyz@gmail.com") 
        self.tearDown()

system = None
def setUp():
    global system
    role = Role(name=Name("admin"))
    role.save()
    role = Role(name=Name("user"))
    role.save()
    
    admin_user = User(name=Name("abc"), 
                      email=Email("abc@gmail.com"), 
                      role=Role.get_by_id(1))
    System.created =False
    admin_user.save() 
    system = System()      
    s = Session(user = admin_user)
    system.session_set.append(s)
    system.user_set = User.get_all()
def tearDown():
    global system
    system.user_set =[]

class TestSystem(TestCase):
    TESTING = True
    

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        setUp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        tearDown()
    
    def test_system_creation(self):
        print "test_system_creation"
        global system
        new_users = system.user_set
        new_user = new_users[0]
        self.assertEquals(new_user.email, "abc@gmail.com")

    def test_add_user(self):
    	print "add_user"
    	global system
        usr = User(name=Name("def"), 
                email=Email("def@gmail.com"), 
                role=Role.get_by_id(2))
        old_users= system.user_set
        administrator = filter(lambda x: x.user.role.name == "admin", system.session_set)
        system.add_user(usr,administrator[0])
        self.assertEqual(len(old_users),len(system.user_set))

    def test_get_email_of_user_valid(self):
        print "test_get_email_of_user"
        global system
        usr = User(name=Name("qwe"), 
                email=Email("qwe@gmail.com"), 
                role=Role.get_by_id(2))
        usr.save()
        system.user_set.append(usr)
        e = system.get_email_of_user(usr)
        self.assertEqual(e, usr.email)


    def test_get_name_of_user_valid(self):
        print "test_get_email_of_user"
        global system
        usr = User(name=Name("qwe"), 
                email=Email("qwe@gmail.com"), 
                role=Role.get_by_id(2))
        usr.save()
        system.user_set.append(usr)
        e = system.get_name_of_user(usr)
        self.assertEqual(e, usr.name)

    def test_get_user_by_email_valid(self):
    	print "test_get_user_by_email"
    	global system
        usr = User(name=Name("pqr"), 
                email=Email("pqr@gmail.com"), 
                role=Role.get_by_id(1))
        usr.save()
        system.user_set = User.get_all()
        u = system.get_user_by_email(usr.email)
        e=u.email
        self.assertEqual(e, usr.email)

    def test_del_user(self):
        print "test_del_user"
        global system
        usr = User(name=Name("qw"), 
                email=Email("e2@gmail.com"), 
                role=Role.get_by_id(2))
        administrator = filter(lambda x: x.user.role.name == "admin", system.session_set)
        system.add_user(usr,administrator[0])
        old_users= system.user_set
        system.del_user(usr,administrator[0])
        self.assertEqual(len(old_users),len(system.user_set))

    def test_get_all_users(self):
        print "test_get_all_users"

if __name__ == '__main__':
    unittest.main()
