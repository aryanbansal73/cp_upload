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
load_dotenv(override=True)
from database import Util

login_obj =  Util("user")


login_blueprint = Blueprint('login', __name__)


# login_blueprint.config['MAIL_SERVER']='smtp.gmail.com'
# login_blueprint.config['MAIL_PORT'] = 465
# login_blueprint.config['MAIL_USERNAME'] = os.getenv("gmail_id")
# login_blueprint.config['MAIL_PASSWORD'] = os.getenv('gmail_pass')
# login_blueprint.config['MAIL_USE_TLS'] = False
# login_blueprint.config['MAIL_USE_SSL'] = True

db_name  = os.getenv("db_name")
collection_name = os.getenv("collection_name")
 
@login_blueprint.route("/", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("login.logged_in"))
    if request.method == "POST":
        
        user = request.form.get("username")
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        # if(check(email)==False):
        #     message = 'The Email entered in not correct , correct and try again'
        #     return render_template('index.html', message=message)
        # if(validate_password(password1)== 0):
        #     message = 'Password does not meet requirements.'
        #     return render_template('index.html', message=message)
        #if found in database showcase that it's found 
        user_found = login_obj.search_doc("User", {"user_name":user})
        email_found = login_obj.search_doc("User",{"email": email})

        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'user_name': user,'name':fullname, 'email': email, 'password': hashed ,  'confirmed': False , 'confirmed_on':None, "codeforces_id_list": {}}
            #insert it in the record collection
            login_obj.insert_doc("User" ,user_input)
            token  = generate_confirmation_token(email)
            print(token)
            confirm_url =  url_for('login.confirm_email' , token =  token, _external = True)
            # print(confirm_url)
            html = render_template('auth_mail.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            #find the new created account and its email
            # user_data = records.find_one({"email": email})
            # send_email(user_data['email'], subject, html)
            flash('A confirmation email has been sent via email.', 'success')

            #if registered redirect to logged in as the registered user
            message ="waiting for id to be confirmed"
            return render_template('confirm_pending.html' , message = message)
            # return render_template('logged_in.html', email=email)
    return render_template('index.html')

@login_blueprint.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
        

    else:
        return redirect(url_for("login.login"))
@login_blueprint.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("login.logged_in"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if(check(email)==False):
            message = 'The Email entered in not correct , correct and try again'
            return render_template('index.html', message=message)
        #check if email exists in database
        user = login_obj.search_doc("User", {"email": email})

        if user:
            email_val = user['email']
            passwordcheck = user['password']
            #encode the password and check if it matches
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                if(user["confirmed"] ==False):
                    message ="waiting for id to be confirmed"
                    return render_template('confirm_pending.html' , message = message)
                else:
                    return redirect(url_for("login.logged_in"))
            else:
                if "email" in session:
                    return redirect(url_for("login.logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
        
    return render_template('login.html', message=message)



@login_blueprint.route("/logout", methods=["POST", "GET"])
def logout():

    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return redirect(url_for("login.index"))


@login_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        message ="The confirmation link is invalid or has expired."
        return render_template('confirm_pending.html' , message = message)
    user =  login_obj.search_doc("User",{"email":email})
    # print(user['confirmed'])
    if(user ==None ):
        message ="The confirmation link is invalid or has expired."
        return render_template('confirm_pending.html' , message = message)
    if user['confirmed']:
        flash('Account already confirmed. Please login.', 'success')
        return render_template('logged_in.html')
    else :
        user['confirmed'] = True 
        user['confirmed_on']= datetime.datetime.now()
        login_obj.update_doc("User" , user ) 
        user1 =  login_obj.search_doc("User",{"email":email})
        print(user1)

    return render_template('logged_in.html')
  


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=" sender='peter@mailtrap.io'"
    )
    with current_app.app_context():
        mail = Mail()
        mail.send(msg)    



def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return 1
 
    else:
        return 0
def validate_password(password):
    # Check if the password has at least 8 characters
    # if len(password) < 8:
    #     return False
    
    # # Check if the password contains at least one uppercase letter
    # if not re.search(r'[A-Z]', password):
    #     return False
    
    # # Check if the password contains at least one lowercase letter
    # if not re.search(r'[a-z]', password):
    #     return False
    
    # # Check if the password contains at least one digit
    # if not re.search(r'\d', password):
    #     return False
    
    # # Check if the password contains at least one special character
    # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #     return False
    
    # If all the conditions are met, the password is valid
    return True