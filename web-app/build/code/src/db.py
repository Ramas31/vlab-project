
# -*- coding: utf-8 -*-

from collections import OrderedDict

from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app, request
from sqlalchemy.orm import relationship
import sqlalchemy.types as types

import os
import re
from urlparse import urlparse
from datetime import datetime
import json

from op_exceptions import AttributeRequired

from utils import *

db = SQLAlchemy()


# Abstract class to hold common methods
class Entity(db.Model):

    __abstract__ = True

    # save a db.Model to the database. commit it.
    def save(self):
        db.session.add(self)
        db.session.commit()

    # update the object, and commit to the database
    def update(self, **kwargs):
        for attr, val in kwargs.iteritems():
            setter_method = "set_" + attr
            try:
                self.__getattribute__(setter_method)(val)
            except Exception as e:
                raise e

        self.save()

    #print "Setting new val"
    #print "Calling %s on %s" % (method_to_set, curr_entity)
    #try:
    #    getattr(record, method_to_set)(new_val)
    #except Exception as e:
    #pass

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Name(object):
    value = None
    def __init__(self, value):
        # value: String 
        # if the string contains any non-alphabet and non-space character,
        # raise a type error
        if is_alphabetic_string(value):
            self.value = value
        else:
            raise TypeError('%s is not a Name!' % value)

    def __str__(self):
        return self.value
    def to_client(self):
        return {
            'name': self.name,
        }

class Email(object):
    value = None
    def __init__(self, value):
        if not is_email(value):
            raise TypeError('%s is not an email!' % value)
        self.value = value

    def __str__(self):
        return self.value

    def to_client(self):
        return {
            'email': self.email
        }

class User(Entity):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, **kwargs):
        if 'email' not in kwargs:
            raise AttributeRequired("email is mandatory")

        if 'name' not in kwargs:
            raise AttributeRequired("name is mandatory")

        if 'role' not in kwargs:
            raise AttributeRequired("Atleast one role is mandatory")

        self.set_email(kwargs['email'])
        self.set_name(kwargs['name'])
        self.set_role(kwargs['role'])

    def set_role(self, role):
        if not isinstance(role, Role):
            raise TypeError('`role` argument should be of type Role.')
        else:
            self.role = role

    def set_email(self, email):
        if not isinstance(email, Email):
            raise TypeError('`email` argument should be of type Email.')
        else:
            self.email = email.value

    def set_name(self, name):
        if not isinstance(name, Name):
            raise TypeError('`name` argument should be of type Name.')
        else:
            self.name = name.value

    def set_role(self, role):
        if not isinstance(role, Role):
            raise TypeError('`role` argument should be of type Role.')
        else:
            self.role = role

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role.to_client()
        }

class Role(Entity):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    users = db.relationship('User', backref='role')

    def __init__(self, **kwargs):
        if 'name' not in kwargs:
            raise AttributeRequired("name is mandatory")

        self.set_name(kwargs['name'])

    def set_name(self, name):
        if not isinstance(name, Name):
            raise TypeError('`name` argument should be of type Name.')
        else:
            self.name = name.value

    def set_users(self, users):
        type_error = False
        for user in users:
            if not isinstance(user, User):
                type_error = True
                break

        if not type_error:
            self.users = users
        else:
            raise TypeError('`user` argument should be of type User.')

    def get_name(self):
        return self.name

    def get_users(self):
        return self.users

    def get_id(self):
        return self.id

    @staticmethod
    def get_by_id(id):
        return Role.query.get(id)

    @staticmethod
    def get_all():
        return Role.query.all()

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Session():
    user=None

    def __init__(self, **kwargs):
        if 'user' not in kwargs:
            raise AttributeRequired("user is mandatory")
        else:
            self._set_user(kwargs['user'])


    def get_user(self):
        return self.user

    def _set_user(self, user):
        if not isinstance(user, User):
            raise TypeError('`user` argument should be of type User.')
        else:
            self.user = user

    def to_client(self):
        pass
        return{
            'user' : self.user.to_client()
        }

from sets import Set
class System(object):

    user_set = []
    session_set = []
    created = False

    def __init__(self):
        if System.created == True:
            raise ConstraintError("System has already been created")
        else:
            #role = Role(name=Name("admin"))
            #role.save()
            #role = Role (name = Name ("user"))
            #role.save()
            self.session_set = []
            self.user_set = []
            System.created = True
            '''admin_user = User(name=Name("abc"), 
                         email=Email("abc@gmail.com"), 
                         role=Role.get_by_id(1))
            admin_user.save()       
            self.user_set.append(admin_user)
            self.user_set = User.get_all()
            for u in self.user_set:
                print u.to_client()
            s = Session(user = admin_user)
            self.session_set.append(s)
            self.user_set = User.get_all()'''

    def start_session(self, email):
    	loggedin_user = filter(lambda x: x.email == email, self.user_set)
        if loggedin_user :
            s = Session (user = loggedin_user[0])
            self.session_set.append(s)
            for i in self.session_set:
                i.to_client()
    	    self.user_set = User.get_all()
        else:
            raise TypeError("user does not exists")

    def stop_session(self, email):
    	loggedin_user = filter(lambda x: x.user.email == email, self.session_set)
        if loggedin_user :
            self.session_set.remove(loggedin_user[0])
    	    self.user_set = User.get_all()
        else:
            raise TypeError("user does not exists")

    def add_user(self, user, session):
        if not session.user.role.name == "admin":
            raise TypeError("only a user with admin role can add")
        else:
            existing_user = filter(lambda x: x.email == user.email, self.user_set)
            if not existing_user :
                self.user_set.append(user)
                user.save()
            else:
                raise TypeError("user already exists")

    def get_email_of_user(self,user):
    	self.user_set = User.get_all() 
        if user in self.user_set:
            return user.email
        else:
            raise TypeError('User does not exist')

    def get_name_of_user(self,user):
    	self.user_set = User.get_all() 
        if user in self.user_set:
            return user.name
        else:
            raise TypeError('User does not exist')

    def get_user_by_email(self,email):
       user_with_required_email = filter(lambda x: x.email == email, self.user_set)

       if user_with_required_email:
            return user_with_required_email[0]
       else:
            raise TypeError('Email does not exist')

    def make_user(self,n,e,r,session):
        if(session.role ==Role.admin):
            user =User(name=n,email=e,role=r)
            self.add_user(user,session)
        else:
            raise ConstraintError("only admin is allowed to create a user")

#+BEGIN_SRC python :tangle ../../src/db.py :eval no
    global flag 
    flag = True

    def del_user(self, user, session):
        if not session.user.role.name == "admin":
           raise TypeError("only a user with admin role can add")
        else:
            if not user.role.name == "admin":
            	self.user_set = User.get_all() 
                users_not_to_be_deleted = filter(lambda x: x.email != user.email, self.user_set)
                user_set=users_not_to_be_deleted
                user.delete()
            else:
                raise TypeError("Admin cannot delete another admin")

    def get_all_users(self):
    	self.user_set = User.get_all();
        return self.user_set

    def get_all_sessions(self):
        return self.session_set

    def get_session(self,sess):
        return filter(lambda x: x.user.email == sess.user.email, self.session_set)
        
    def get_session_from_email(self,e):
        return filter(lambda x: x.user.email == e, self.session_set)

	def add_session(self,u):
		sess = Session(user = u)
        self.session_set.append(sess)
        return sess

    def set_user(self,user):
        self.session_set.append(user)

    def del_sessions(self,user,session):
        session_to_be_deleted = filter(lambda x: x.user.email == user.email, self.session_set)
        if len(session_to_be_deleted):
            self.session_set.remove(session_to_be_deleted)
        else:
            raise ConstraintError("user does not exist")

#system = System() # THIS WILL CAUSE ERROR SINCE THERE ARE db OPERATION IN
                   # AND db IS NOT CREATED AT POINT.
