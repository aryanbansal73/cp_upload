from flask import Flask, redirect, url_for, session, render_template, request,flash , Blueprint  ,current_app
import bcrypt
import pymongo
from database import connect_db
import re 
from src.token_1 import generate_confirmation_token, confirm_token
from flask_mail import Message
from flask_mail import Mail
import datetime

import os
from dotenv import load_dotenv
import sys, os.path
dir_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), ))+ '/cp_funcs/')
print(dir_path)
sys.path.append(dir_path)
import main 



user_blueprint = Blueprint('user', __name__)
records =  connect_db()


@user_blueprint.route('/home' ,  methods =['post' , 'get'] )
def home():
    if "email" in session:
        email = session["email"]
        user_found = records.find_one({"email": email})
        cf_ids = user_found['codeforces_id_list']
        new_cf_id =request.form.get("cf_id")
        for i in cf_ids:
            if(i=='' or i==None):
                cf_ids.remove(i)
        print(new_cf_id)
        if(new_cf_id =='' or new_cf_id   in cf_ids):
            return render_template('home.html' , cf_id_list =cf_ids )
        if(len(cf_ids)==0):
            print('empty')
            cf_ids.append(new_cf_id)
        else:
            cf_ids.append(new_cf_id)
            print(cf_ids)
        
        user_found['codeforces_id_list'] = cf_ids
        records.update_one({'_id':user_found['_id']}, {'$set':user_found} )
        return render_template('home.html' , cf_id_list =cf_ids )

    else:
        return redirect(url_for("login.login"))
    return render_template('home.html')

@user_blueprint.route('/home/<cf_id>')
def options(cf_id):
    return render_template('features_base.html' ,cf_id = cf_id )
@user_blueprint.route('/home/<cf_id>/sync')
def sync_cf(cf_id):
    if "email" in session:
        print('on_hai')
        #uncomment to make the func work
        # email = session["email"]
        # user_found = records.find_one({"email": email})
        # main.module_func(cf_id ,  git_access_token ,  "test123")
        return render_template('process.html')
    else:
        return redirect(url_for(user_page.options))
