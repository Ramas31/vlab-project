
# -*- coding: utf-8 -*-

import os
import csv
import requests
from datetime import datetime
import inspect
from flask import session, render_template, Blueprint, request, jsonify, abort, current_app, redirect, url_for
from config import *
from flask import current_app

from flask import Flask, redirect, url_for
from werkzeug import secure_filename
from db import *
from utils import parse_request, jsonify_list
api = Blueprint('APIs', __name__)

system = System()

@api.route('/users', methods=['GET'])
def get_users():
    global system
    return jsonify_list([i.to_client() for i in system.get_all_users()])

@api.route('/names', methods=['GET'])
def get_names():
    global system
    return jsonify_list([i.to_client()['name'] for i in system.get_all_users()])

@api.route('/roles', methods=['GET'])
def get_roles():
    return jsonify_list([i.to_client() for i in Role.get_all()])

@api.route('/emails', methods=['GET'])
def get_emails():
    global system
    return jsonify_list([i.to_client()['email'] for i in system.user_set])

@api.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        if ('email' in session):
            return render_template("user-list.html")
        else:
            return render_template("login.html")

@api.route("/auth/login", methods=['GET', 'POST'])
def login():
    global system
    if request.method == 'POST':
        email = str(request.form['email'])
      
        url_for_getting_the_user = "%s/users" % \
                                   (APP_URL)
        backend_resp = requests.get(url_for_getting_the_user)
        user_list = backend_resp.json()
        if len(backend_resp.text.encode('ascii')) != 2:
            count = 0
            for user in range(len(user_list)):
                print len(user_list)
                print user_list[user]
                if str(email) == str(user_list[user]['email']):
                    current_app.logger.info("Successfully Logged in")
                    session['email'] = email
                    System.start_session(system,email)
                    session['role_name'] = str(user_list[user]['role']['name'])
                    return redirect("/")
                else:
                    count = count + 1
            if count == len(user_list):
                return render_template("login.html", message="Invalid email id")
            
@api.route('/auth/logout', methods=['GET'])
def logout_handler():
    global system
   
    e= session.pop('email', None)
    System.stop_session(system,e)
    session.pop('role_name', None)
   
    return redirect("/")

@api.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    
    record = User.get_by_id(id)
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("user", id))
    return jsonify(record.to_client())

@api.route('/roles/<int:id>', methods=['GET'])
def get_role_by_id(id):
    record = Role.get_by_id(id)
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("role", id))
						
    return jsonify(record.to_client())

@api.route('/users/<int:id>/email', methods=['GET'])
def get_email_by_id(id):
    global system
    record = User.get_by_id(id)
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("email", id))
    else:
        d = {}
        d['email'] = system.get_email_of_user(record) 
        return jsonify(d)

@api.route('/users/<int:id>/name', methods=['GET'])
def get_name_by_id(id):
    global system
    record  = User.get_by_id(id)
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("name", id))
    else:
        d= {}
        d['name'] = system.get_name_of_user(record) 
        return jsonify(d)

@api.route('/users', methods=['POST'])
def create_user():
   ### Check if there is a session and act according to the specification
    global system
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400)
    else:
        name = request.json['name']
        email = request.json['email']
        role_id = request.json['role_id']
        session_email = request.json['session']
        try:
            ses = system.get_session_from_email(session_email)
            session = ses[0]
            user = User(name=Name(name),
                        email=Email(email),
                        role=Role.get_by_id(role_id))
	    System.add_user(system,user,session)
            return jsonify(user.to_client())
        except Exception, e:
            current_app.logger.error("Error occured while inserting"
                                     "user record: %s" % str(e))
            abort(500, str(e))

@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    global system
    ### Check if there is a session and act according to the specification
    if id==0:
    	abort(500)
    else:
        session_email = request.headers.get('session')
        try:
            ses = system.get_session_from_email(session_email)
            session = ses[0]
            user = User.get_by_id(id)
	    System.del_user(system,user,session)
            return jsonify(id= id,status = 'success')

        except Exception, e:
            current_app.logger.error("Error occured while inserting"
                                     "user record: %s" % str(e))
            abort(500, str(e))

@api.route('/users/<int:id>', methods=['PUT'])
def update_delete_user(id):
    global system
    ### Check if there is a session and act according to the specification
    if 'session' not in request.json:
        print "throw error"
    else:
        print "Check according to your specification"

    record = User.get_by_id(id)
    if not record:
        abort(404, 'No %s with id %s' % (user, id))


    if request.method == 'PUT':

        new_data = {}
        try:
            if 'name' in request.json:
                new_data['name'] = Name(request.json['name'])
            if 'email' in request.json:
                new_data['email'] = Email(request.json['email'])
            if 'role_id' in request.json:
                role = Role.get_by_id(request.json['role_id'])
                new_data['role'] = role

            record.update(**new_data)

            return jsonify(User.get_by_id(id).to_client())

        except Exception, e:
            current_app.logger.error("Error occured while updating"
                                     " user record %d: %s" % (id, str(e)))
            abort(500, str(e))

@api.route('/users/<string:email>', methods=['GET'])
def get_user_by_email(email):
    global system
    record = system.get_user_by_email(email)
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("email", id))

    return jsonify(record.to_client())
