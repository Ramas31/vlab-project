
# -*- coding: utf-8 -*-
import unittest
from flask.ext.testing import TestCase
from datetime import datetime	
from src.db import *
from src.app import create_app
from src.op_exceptions import AttributeRequired	
from src.api import * 		
config = {
    'SQLALCHEMY_DATABASE_URI': ''
}

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
        
    def test_get_user_by_id(self):
 	print "test_get_user_by_id"
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=Role.get_by_id(1))
        user1.save()
        headers = {'content-type': 'application/json'}
        response = self.client.get("/users/1",     
                                   headers=headers)
        
        self.assertEqual(response.status_code, 200)
        
    def test_get_email_by_id(self):
 	print "test_get_email_by_id"
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=Role.get_by_id(1))
        user1.save()
        headers = {'content-type': 'application/json'}
        response = self.client.get("/users/1/email",     
                                   headers=headers)
        result = json.loads(response.data)
        self.assertEqual(result['email'], user1.email)
        self.assertEqual(response.status_code, 200)
    
    def test_get_name_by_id(self):
 	print "test_get_name_by_id"
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=Role.get_by_id(1))
        user1.save()
        headers = {'content-type': 'application/json'}
        response = self.client.get("/users/1/name",     
                                   headers=headers)
        result = json.loads(response.data)
        self.assertEqual(result['name'],"admin user")
        self.assertEqual(response.status_code, 200)

    def test_get_all_users(self):
        print "test_get_all_users"

        ###Create Users
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=Role.get_by_id(1))
        user1.save()
        r = self.client.get('/users')
        result = json.loads(r.data)
        self.assertEquals(len(result), 1)

    def test_get_all_names(self):
        print "test_get_all_names"
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        ###Create Users
       
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=Role.get_by_id(1))
        user1.save()
        r = self.client.get('/names')
        result = json.loads(r.data)
        self.assertEquals(len(result), 1)

    def test_get_all_emails(self):
        print "test_get_all_emails"
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        ###Create Users
       
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=Role.get_by_id(1))
        user1.save()
        r = self.client.get('/emails')
        result = json.loads(r.data)
        self.assertEquals(len(result), 1)

    def test_get_all_roles(self):
        print "test_get_all_roles"
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        ###Create Users
       
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=Role.get_by_id(1))
        user1.save()

        headers = {'content-type': 'application/json'}

        response = self.client.get("/roles",
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
       
    def test_get_role_by_id(self):
 	print "test_get_user_by_id"
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=Role.get_by_id(1))
        user1.save()
        headers = {'content-type': 'application/json'}
        response = self.client.get("/roles/1",     
                                   headers=headers)
     
        self.assertEqual(response.status_code, 200)


    def test_get_one_user(self):
        print "test_get_one_user"
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        ### create a User
        
        user1 = User(name=Name("admin user"),
                    email=Email("admin@xyz.com"),
                    role=Role.get_by_id(1))
        user1.save()
        user2 = User(name=Name("normal user"),
                    email=Email("normal@xyz.com"),
                    role=Role.get_by_id(2))
        user2.save()

        r = self.client.get('/users/1')
        result = json.loads(r.data)
        self.assertEqual(result['name'], "admin user")

    def test_update_existing_user(self):
        # Create a user
        # update the same user
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        user1 = User(name=Name("admin user"),
                     email=Email("admin@xyz.com"),
                     role=Role.get_by_id(1))

        user1.save()
        user2 = User(name=Name("normal user"),
                     email=Email("normal@xyz.com"),
                     role=Role.get_by_id(1))

        user2.save()

        payload = {'email': 'ttt@kkk.com',
                   'name': 'nearly normal user',
                   'role_id': 2,
                   'session': 't@g.com'}
        headers = {'content-type': 'application/json'}
        response = self.client.put("/users/2",
                                   data=json.dumps(payload),
                                   headers=headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['name'], "nearly normal user")

    def test_create_new_user(self):
        print "test_create_new_user"
        global system
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        adm = User(name=Name("xyz"), 
                email=Email("xyz@gmail.com"), 
                role=Role.get_by_id(1))
        adm.save()
        sess = Session(user = adm)
        system.session_set.append(sess)
        system.user_set = User.get_all()
        payload = {'name':'abcde','email':'abcde@gmail.com',
                   'role_id':'2','session':'xyz@gmail.com'}

        headers = {'content-type': 'application/json'}

        response = self.client.post("/users",
                                    data=json.dumps(payload),
                                    headers=headers)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        global system
        print "test_delete_user"
        role1 = Role(name = Name("admin"))
        role1.save()
        role2 = Role(name = Name("user"))
        role2.save()
        user1 = User(name=Name("admin user"),
                     email=Email("admin@xyz.com"),
                     role=Role.get_by_id(1))

        user1.save()
        user2 = User(name=Name("normal user"),
                     email=Email("normal@xyz.com"),
                     role=Role.get_by_id(2))

        user2.save()
        system.session_set = []
        sess = Session(user = user1)
        system.session_set.append(sess)
        system.user_set = User.get_all()
        payload = {'session': 'admin@xyz.com'}

        headers = {'content-type': 'application/json'}

        response = self.client.delete("/users/2",
                                      data=json.dumps(payload),
                                      headers=headers)

        self.assertEqual(response.status_code, 200)
	

if __name__ == '__main__':
    unittest.main()
