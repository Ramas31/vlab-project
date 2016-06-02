
# -*- coding: utf-8 -*-
from op_exceptions import AttributeRequired

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

class Email(object):
    value = None
    def __init__(self, value):
        if is_email(value):
            self.value=value
        else:
            raise TypeError("%s is not an Email" % value)
    def __str__(self):
        return self.value
        

class User():
    users = [] # this is a static variable, accessed by User.users
    name = None
    email = None
    role = None

    def __init__(self, **kwargs):
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                if key == 'name':
                    self.setName(value)
                if key == 'email':
                    self.setEmail(value)
                if key == 'role':
                    self.setRole(value)
            self.users.append(self)

    def setEmail(self, email):
        if isinstance(email, Email):
            self.email=email
        else:
            raise TypeError("%s is not an email" % email)

    def setName(self, name):
        if isinstance(name, Name):
            self.name=name
        else:
             raise TypeError("%s is not an name" % name)

    def setRole(self, role):
        if isinstance(role, Role):
            self.role = role
        else:
            raise TypeError("%s is not an role" % role)

    def getRole(self):
        return self.role

    def getEmail(self):
        return self.email

    def getName(self):
        return self.name

    @staticmethod
    def get_all():
        return User.users

    def to_client(self):
        pass
        return {
            'name': self.name,
            'email': self.email,
            'role': self.role.to_client()
        }

class Role():
    name = None
    admin = None
    user = None

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def to_client(self):
        return {
            'role': self.name
        }

    def to_client(self):
        pass

Role.admin = Role("admin")
Role.user  = Role("user")

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
        return {
            'session': self.user.to_client()
        }

    def update_name(self, u, session, new_name):
        if session in sessions:
            if session.role == Role.admin and u == self.user:
                if isinstance(u,User):
                    u.setName(new_name)
                else:
                    raise TypeError("Not of type User")
            elif session.role == Role.admin:
                if isinstance(u,User) :
                    u.setName(new_name)
                else:
                    raise TypeError("Not of type User")
        else:
            raise TypeError("User does not have a session")

    def update_email(self,u, session, new_email):
        if session.user in sessions:
            if session.role == "user" and u == self.user:
                if isinstance(u,User):
                    u.setName(new_email)
                else:
                    raise TypeError("Not of type User")
            elif session.role == Role.admin:
                if isinstance(u,User) :
                    u.setName(new_name)
                else:
                    raise TypeError("Not of type User")
        else:
            raise TypeError("User does not have a session")

    def update_role(self, u, session, new_role):
        if session.user in sessions:
            if session.role == Role.user:
                raise TypeError("only a user with admin role can update role")
            elif session.role == Role.admin:
                if isinstance(u,User) and u.role == Role.admin:
                    u.setRole("admin")
                else:
                    raise TypeError("Not of type User")
        else:
            raise TypeError("User does not have a session")

    def to_client(self):
        pass
        return{
        'user' : self.user.to_client()
   }

from sets import Set
class System():
    user_set  = Set()
    session_set = Set()
    

    def __init__(self):
        admin_user = User(name=Name("admin"), email=Email("app-admin@vlabs.ac.in"), role=Role.admin)
        self.user_set.add(admin_user)
        self.session_set.add(admin_user)

    def add_user(self, user, session):
        if session.role is not Role.admin:
            raise TypeError("only a user with admin role can add")
        else:
            existing_user = filter(lambda x: x.email.value == user.email.value, self.user_set)
            if not existing_user :
                self.user_set.add(user)
            else:
                raise TypeError("user already exists")

    def get_email_of_user(self,user):
        if user in self.user_set:
            return user.email.value
        else:
            raise TypeError('User does not exist')

    def get_name_of_user(self,user):
        if user in self.user_set:
            return user.name.value
        else:
            raise TypeError('User does not exist')

    def get_user_by_email(self,email):
        user_with_required_email = filter(lambda x: x.email.value == email.value, self.user_set)
        if user_with_required_email:
            return user_with_required_email[0]
        else:
            raise TypeError('Email does not exist')

    def make_user(self,n,e,r,session):
        if(session.user.role ==Role.admin):
            user =User(name=n,email=e,role=r)
            self.add_user(user,session)
        else:
            raise ConstraintError("only admin is allowed to create a user")

#+BEGIN_SRC python :tangle ../../src/obj.py :eval no
    global flag 
    flag = True

    def del_user(self, user, session):
        if session.role is not Role.admin:
           raise TypeError("only a user with admin role can add")
        else:
            if user.role is not Role.admin:
                user_to_be_deleted = filter(lambda x: x.email.value == user.email.value, self.user_set)
                self.user_set.remove(user_to_be_deleted[0])
            else:
                raise TypeError("Admin cannot delete another admin")

    def get_all_users(self):
        return self.user_set

    def get_all_sessions(self):
        return self.session_set

    def get_session(self,user):
        return filter(lambda x: x.email.value == user.email.value, self.session_set)

    def set_user(self,user):
        self.session_set.add(user)

    def del_sessions(self,user,session):
        session_to_be_deleted = filter(lambda x: x.email == user.email, self.session_set)
        if len(session_to_be_deleted):
            self.session_set.remove(session_to_be_deleted)
        else:
            raise ConstraintError("user does not exist")
