from flask import Flask, redirect, url_for, session, render_template, request,flash , Blueprint  ,current_app
import bcrypt
import pymongo
import re 
from src.token_1 import generate_confirmation_token, confirm_token
from flask_mail import Message
from flask_mail import Mail
import datetime

import os
from dotenv import load_dotenv
import sys, os.path
dir_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), ))+ '/cp_funcs/')
sys.path.append(dir_path)
import sync 
git_access_token= os.getenv("git_access_token")
db_name  = os.getenv("db_name1")
# "User" = os.getenv(""User"1")
from database import Util

user_obj =  Util("user")

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/home', methods=['post', 'get'])
def home():
    if "email" in session:
        email = session["email"]
        user_found = user_obj.search_doc("User", {"email": email})
        cf_ids = user_found.get('codeforces_id_list', {})  # Initialize as an empty dictionary if not present
        new_cf_id = request.form.get("cf_id")
        print(cf_ids)
        # Create a list to store keys to be removed
        keys_to_remove = []

        for key, value in cf_ids.items():
            if  key == None or key =="" or key.isspace():  # Remove empty or None values
                keys_to_remove.append(key)
                continue

        # Remove keys marked for removal
        for key in keys_to_remove:
            del cf_ids[key]


        if not new_cf_id or new_cf_id in cf_ids:
            return render_template('home.html', cf_id_list=cf_ids)

        if not cf_ids:
            print('empty')
            cf_ids[new_cf_id] = []
        else:
            cf_ids[new_cf_id] = []

        user_found['codeforces_id_list'] = cf_ids
        user_obj.update_doc("User", user_found)
        return render_template('home.html', cf_id_list=cf_ids)

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
        email = session["email"]
        user_found = user_obj.search_doc("User",{"email": email})
        client = user_obj.give_db()
        records =  client["user"]["User"]
        sync.module_func(cf_id ,  git_access_token ,records,email,  "test123")
        user_obj.close_db(client)
        return render_template('process.html')
    else:
        return redirect(url_for("login.login" ))
