from flask import Flask, redirect, url_for, session, render_template, request,flash
import bcrypt
import pymongo
from dotenv import load_dotenv
from src.token_1 import generate_confirmation_token, confirm_token
import os
from flask_mail import Mail
import re 
import time


import datetime
from flask_mail import Message
app = Flask(__name__)
app.secret_key = "testing1"
# configuration of mail 
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '9e9a60933a6aa9'
app.config['MAIL_PASSWORD'] = 'c174316eaa9f23'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail =  Mail(app)
load_dotenv()

# Retrieve sensitive information from environment variables
db_pass = os.getenv('db_pass')

# Ensure that the required environment variable is set
if db_pass is None:
    raise ValueError("DB_PASS environment variable not set.")
else:
    print(db_pass)
# MongoDB connection setup
connection_url = f"mongodb+srv://whathwaye:{db_pass}@cluster0.gsuq52o.mongodb.net/?retryWrites=true&w=majority"
db_name = 'test1'
client = pymongo.MongoClient(connection_url)
db = client[db_name]
collection_name = 'test1'
records = db[collection_name]

# Your Flask routes and other code go herea

# @app.route("/", methods=['post'])
# def func():
#     if request.method == "POST":
#         user = "ary" 
#         email = "ffs" 
#         hashed = "sgjslg"
#         user_input = {'name': user, 'email': email, 'password': hashed}
#         db['test1'].insert_one(user_input)
#         return "congrats"
# #assign URLs to have a particular route 
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        
        user = request.form.get("username")
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if(check(email)==False):
            message = 'The Email entered in not correct , correct and try again'
            return render_template('index.html', message=message)
        if(validate_password(password1)== 0):
            message = 'Password does not meet requirements.'
            return render_template('index.html', message=message)
        #if found in database showcase that it's found 
        user_found = records.find_one({"user_name": user})
        email_found = records.find_one({"email": email})

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
            user_input = {'user_name': user,'name':fullname, 'email': email, 'password': hashed ,  'confirmed': False , 'confirmed_on':None, "codeforces_id_list": []}
            #insert it in the record collection
            records.insert_one(user_input)
            token  = generate_confirmation_token(email)
            print(token)
            confirm_url =  url_for('confirm_email' , token =  token, _external = True)
            html = render_template('auth_mail.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            send_email(user_data['email'], subject, html)
            flash('A confirmation email has been sent via email.', 'success')

            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user =  records.find_one({"email":email})
    print(user['confirmed'])
    if user['confirmed']:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user['confirmed'] = True 
        user['confirmed_on']= datetime.datetime.now()
        # print(user)
        records.update_one({'_id':user['_id']}, {'$set':user} ,  upsert= False) 
        user1 =  records.find_one({"email":email})
        print(user1)

    return render_template('login.html')
@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if(check(email)==False):
            message = 'The Email entered in not correct , correct and try again'
            return render_template('index.html', message=message)
        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
        

    else:
        return redirect(url_for("login"))
@app.route('/home' ,  methods =['post' , 'get'] )
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
        return redirect(url_for("login"))
    return render_template('home.html')
@app.route("/logout", methods=["POST", "GET"])
def logout():

    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return redirect(url_for("index"))

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
    if len(password) < 8:
        return False
    
    # Check if the password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    
    # Check if the password contains at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False
    
    # Check if the password contains at least one digit
    if not re.search(r'\d', password):
        return False
    
    # Check if the password contains at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    # If all the conditions are met, the password is valid
    return True
def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=" sender='peter@mailtrap.io'"
    )
    mail.send(msg)


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)