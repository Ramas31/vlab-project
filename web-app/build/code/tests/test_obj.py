
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from datetime import datetime

from src.op_exceptions import AttributeRequired
from src.obj import *

class TestName1(TestCase):
    TESTING = True
    def test_name_type(self):
        print "test_name_type"
        new_name = Name("John")
        # correct name
        self.assertEqual(new_name.value, "John")
        # incorrect name
        self.assertEqual(new_name.value, "123dasd")

class TestName2(TestCase):
    TESTING = True
    def test_name_type(self):
        print "test_name_type"
        new_name = Name("John")
        self.assertEqual(new_name.value, "J@67697vjhdcs")

class TestName3(TestCase):
    TESTING = True
    def test_name_type(self):
        print "test_name_type"
        new_name = Name("John")
        self.assertEqual(new_name.value, "#$%&^   HKJ   5678")

class TestEmail1(TestCase):
    TESTING = True
    def test_email_type(self):
        print "test_name_type"
        new_email = Email("abc@gmail.com")
        # correct email
        self.assertEqual(new_email.value,"abc@gmail.com")
        # incorrect email
        self.assertEqual(new_email.value,"abc@vmnv@gmail.com")       

class TestEmail2(TestCase):
    TESTING = True
    def test_email_type(self):
        print "test_name_type"
        new_email = Email("abc@gmail.com")
        self.assertEqual(new_email.value, "qww@fnbnm")    

class TestEmail3(TestCase):
    TESTING = True
    def test_email_type(self):
        print "test_name_type"
        new_email = Email("abc@gmail.com")
        self.assertEqual(new_email.value,"abcgmail.com")
        

class TestUser(TestCase):
    TESTING = True

    def test_user_creation(self):
        print "test_user_creation"
        new_user = User(email = Email("abc@gmail.com"),name = Name("abc"),role = Role.admin)
        self.assertEqual(new_user.email.value, "abc@gmail.com")
        self.assertEqual(new_user.name.value, "abc")
        self.assertEqual(new_user.role, Role.admin)
        self.assertRaises(TypeError,User,name = Name("abc"),email = Email("abc@gmail.com"),role = Role.admin)

    def test_user_creation_without_role(self):
        print "test_user_creation_without_email"
        with self.assertRaises(AttributeRequired):
            user=User(name=Name("abc"),email=Email("abc@gmail.com"))

    def test_user_creation_without_email(self):
        print "test_user_creation_without_role"
        with self.assertRaises(AttributeRequired):
            user=User(name=Name("abc"),role=Role("admin"))  

    def test_user_creation_without_email_and_role(self):
        print "test_user_creation_without_role_and_email"
        with self.assertRaises(AttributeRequired):
            user=User(name=Name("abc")) 

    def test_user_creation_with_role(self):
        print "test_user_creation_with_role"
        with self.assertRaises(TypeError):
            user=User(name=Name("abc"),email=Email("abc@gmail.com"),role=Role("admin"))

    def test_user_get_all(self):
        print"test get all"
        user1 = User(name=Name("abc"), email = Email("abc@gmail.com"),
        role=Role("admin"))
        user2 = User(name=Name("pqr"), email = Email("pqr@gmail.com"),
        role=Role("user"))
        new_user = User.get_all()
        self.assertEqual(User.users, new_user)

    def test_set_email(self):
        print"test_set_email"
        user = User(name=Name("abc"), email = Email("abc@gmail.com"),
        role=Role("admin"))
        user.setEmail(Email("abc@gmail.com"))
        self.assertEqual(user.email, "abc@gmail.com")

    def test_set_Name(self):
        print"test_set_email"
        user = User(name=Name("abc"), email = Email("abc@gmail.com"),
        role=Role("admin"))
        user.setName(Name("abc"))
        self.assertEqual(user.name, "abc")

    def test_set_role(self):
        print"test_set_email"
        user = User(name=Name("abc"), email = Email("abc@gmail.com"),
        role=Role("admin"))
        user.setRole(Role("admin"))
        self.assertEqual(user.role, "admin")

    def test_get_role(self):
        print"test get role"
        user = User(name=Name("abc"), email = Email("abc@gmail.com"),
        role=Role("admin"))
        new_role = user.getRole()
        self.assertEqual(new_role.name, user.role.name)

    def test_get_email(self):
        print"test get email"
        user = User(name=Name("abc"), email = Email("abc@gmail.com"),
        role=Role("admin"))
        new_email = user.getEmail()
        self.assertEqual(new_email, user.email)

    def test_get_name(self):
        print"test get name"
        user = User(name=Name("abc"), email = Email("abc@gmail.com"),
        role=Role("admin"))
        new_name = user.getName()
        self.assertEqual(new_name, user.name)

class test_role_set_name(TestCase):
    def test_role_type(self):
        print "test_role_type"
        new_role = Role.admin
        self.assertEqual(new_role, Role.admin)
    def test_role_type1(self):
        print "test_role_type"
        new_role = Role.user
        self.assertEqual(new_role, Role.user)
    

class TestSession(TestCase):
    TESTING = True
    s=System()

class TestSystem(TestCase):
    s = System()
    adm =User(name=Name("ghi"),email=Email("app-admin2@vlabs.ac.in"),role=Role.admin)
    System.user_set.add(adm)
    System.session_set.add(adm)
    user=User(name=Name("abc"),email=Email("app-user@vlabs.ac.in"),role=Role.user)
    user2=User(name=Name("def"),email=Email("app-user2@vlabs.ac.in"),role=Role.user)



    TESTING = True
    def test_add_user(self):
        print "test_add_user"
        old_users= System.user_set
        administrator= filter(lambda x: x.role == Role.admin, System.session_set)
        sess = self.s.get_session(administrator[0])
        System.add_user(self.s,self.user,sess[0])
        self.assertEqual(len(old_users),len(System.user_set))


    def test_get_email_of_user_valid(self):
        print "test_get_email_of_user"
        e = System.get_email_of_user(self.s,self.user)
        self.assertEqual(e, self.user.email.value)

    def test_get_email_of_user_invalid(self):
        print "test_get_email_of_user"
        e = System.get_email_of_user(self.s,self.user2)
        self.assertEqual(e, self.user.email.value)

    def test_get_name_of_user_valid(self):
        print "test_get_name_of_user"
        n = System.get_name_of_user(self.s,self.user)
        self.assertEqual(n, self.user.name.value)

    def test_get_name_of_user_invalid(self):
        print "test_get_name_of_user"
        n = System.get_name_of_user(self.s,self.user2)
        self.assertEqual(n, self.user.name.value)


    def test_get_user_by_email_valid(self):
        print "test_get_user_by_email"
        u = System.get_user_by_email(self.s,self.user.email)
        e=u.email.value
        self.assertEqual(e, self.user.email.value)

    def test_get_user_by_email_invalid(self):
        print "test_get_user_by_email"
        u = System.get_user_by_email(self.s, self.user2.email)
        self.assertEqual(u.email.value, self.user.email.value)

    def test_del_user(self):
        print "test_del_user"
        old_users = System.user_set
        administrator= filter(lambda x: x.role == Role.admin, System.session_set)
        user3=User(name=Name("jkl"),email=Email("app-user3@vlabs.ac.in"),role=Role.user)
        sess = self.s.get_session(administrator[0])
        System.add_user(self.s,user3,sess[0])
        System.del_user(self.s,user3,sess[0])
        self.assertEqual(len(old_users),len(System.user_set))

    def test_make_user(self):
        print "test_make_user"

    def test_get_all_users(self):
        print "test_get_all_users"


    def tearDown(self):
        pass
    

    def test_system_creation(self):
        print "test_system_creation"
        admin_user = User(name=Name("admin"),email=Email("app-admin@vlabs.ac.in"),role=Role.admin)
        new_user = System.user_set.pop()
        self.assertEquals(new_user.email.value, admin_user.email.value)
        

if __name__ == '__main__':
    unittest.main()
